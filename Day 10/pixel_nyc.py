#!/usr/bin/env python3
"""
New York, pixel-art edition  ·  #30DayMapChallenge  ·  "make AI work for its money"

Real geodata -> GeoPandas -> a strict 800x880 pixel canvas (no anti-aliasing)
-> pixel textures / sprites / pixel fonts -> nearest-neighbour upscale x4.
No image generator anywhere: every pixel comes from code.

  1. fetch     open datasets from GitHub mirrors
  2. project   UTM 18N (metres); 1 canvas pixel ~ 81 m
  3. simplify  generalise geometry
  4. palette   one fixed Stardew-Valley-ish palette (~40 colours)
  5. raster    matplotlib with antialiasing OFF -> exact palette pixels
  6. pixelfx   grass tufts, water sparkle, pixel trees, landmark sprites
  7. ui        pixel fonts, parchment panels, legend, scale bar
  8. export    nearest-neighbour x4 -> PNG
"""
import io, os, zipfile, urllib.request, warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely import affinity
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA, FONTS = os.path.join(HERE, "data"), os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "pixel_nyc.png")
OUT_SMALL = os.path.join(HERE, "pixel_nyc_1x.png")
CRS = "EPSG:32618"
rng = np.random.default_rng(11)
PW, PH, SCALE = 800, 880, 4          # canvas pixels, upscale factor


def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ----------------------------------------------------------------------------
# PALETTE - Stardew-ish: sunny grass, dirt paths, river blues, wooden UI
# ----------------------------------------------------------------------------
PAL = dict(
    # water
    w0="#2c5a99", w1="#3b78b3", w2="#4f95c8", w3="#9bd0ea",
    # NYC land
    g0="#78b04a", g1="#689c3e", g2="#8cc25a", marsh="#5f9f7a",
    park="#4a8838", tree_d="#2f6a2c", tree_l="#62a84a",
    street="#cfa46a", avenue="#a8723d", town="#e8d5a6", hwy="#b9b09f", hwy_case="#5a3d27",
    subway="#c0432f", station="#fff1c1", airport="#cbc5b6", runway="#8f897c",
    outline="#4a2e1b",
    # surroundings (washed-out copy of the same world)
    c0="#bccb94", c1="#b0c088", c2="#c8d6a2", c_urban="#cdc8a4", c_line="#a4b67c",
    c_road="#dbd1a6", c_text="#68794a",
    # sprites + UI
    red="#d9423a", gold="#f2c230", cream="#fff6dc",
    parch="#f6e2a8", parch_d="#e3c27a", wood="#b7773f", wood_d="#6b3f22", ink="#3a2314",
)
C = {k: rgb(v) for k, v in PAL.items()}


# ----------------------------------------------------------------------------
# 1. FETCH
# ----------------------------------------------------------------------------
def fetch():
    os.makedirs(DATA, exist_ok=True); os.makedirs(FONTS, exist_ok=True)

    def get(url):
        print("  GET", url); return urllib.request.urlopen(url, timeout=300).read()

    zips = {
        "https://codeload.github.com/jdsantos/nyc-geojson-sample-dataset/zip/refs/heads/main": {
            "lines/street-centerline-cscl.geojson": "cscl.geojson",
            "lines/subway-lines.geojson": "subway_lines.geojson",
            "points/subway-stations.geojson": "subway_stations.geojson",
            "polygons/hydrography.geojson": "hydro.geojson",
            "polygons/taxi-zones.geojson": "taxi_zones.geojson"},
        "https://codeload.github.com/ResidentMario/geoplot-data/zip/refs/heads/master": {
            "nyc-boroughs.geojson": "boroughs.geojson"},
    }
    for url, members in zips.items():
        if all(os.path.exists(os.path.join(DATA, v)) for v in members.values()):
            continue
        z = zipfile.ZipFile(io.BytesIO(get(url)))
        for name in z.namelist():
            for suf, local in members.items():
                if name.endswith(suf):
                    open(os.path.join(DATA, local), "wb").write(z.read(name))

    ne = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
    for f, local in [("ne_10m_admin_2_counties", "counties"), ("ne_10m_roads", "roads"),
                     ("ne_10m_urban_areas", "urban")]:
        p = os.path.join(DATA, local + ".geojson")
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            open(p, "wb").write(get(ne + f + ".geojson"))

    gf = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
    for f in ["silkscreen/Silkscreen-Regular.ttf", "vt323/VT323-Regular.ttf"]:
        p = os.path.join(FONTS, os.path.basename(f))
        if not os.path.exists(p):
            open(p, "wb").write(get(gf + f))


# ----------------------------------------------------------------------------
# 2-3. LOAD / PROJECT / SIMPLIFY
# ----------------------------------------------------------------------------
BBOX = (-75.0, 40.0, -73.0, 41.4)


def load(name, bbox=None):
    return gpd.read_file(os.path.join(DATA, name), bbox=bbox).to_crs(CRS)


def smooth(g, simp, rad):
    return g.simplify(simp, preserve_topology=True).buffer(rad, join_style=1).buffer(-rad, join_style=1)


def segs(geoms, tol):
    out = []
    for g in geoms:
        if g is None or g.is_empty:
            continue
        g = g.simplify(tol)
        for part in getattr(g, "geoms", [g]):
            if part.geom_type == "LineString" and len(part.coords) > 1:
                out.append(np.asarray(part.coords))
    return out


def build():
    print("loading + projecting")
    boro, hydro, taxi = load("boroughs.geojson"), load("hydro.geojson"), load("taxi_zones.geojson")
    subl, subs = load("subway_lines.geojson"), load("subway_stations.geojson")
    counties = load("counties.geojson", BBOX)
    roads = load("roads.geojson", BBOX)
    urban = load("urban.geojson", BBOX)
    cscl = load("cscl.geojson")

    nyc_land = smooth(unary_union(boro.geometry), 60, 40)

    # --- the surroundings: NJ, Long Island, Westchester, Connecticut ---------
    nyc_names = {"Bronx", "New York", "Richmond", "Queens", "Kings"}
    ctx = counties[~((counties.REGION == "NY") & counties.NAME.isin(nyc_names))]
    ctx_union = smooth(unary_union(ctx.geometry.buffer(120)), 120, 90)
    ctx_borders = unary_union(ctx.geometry.boundary).intersection(ctx_union.buffer(-260))
    ctx_urban = unary_union(urban.geometry.simplify(120)).intersection(ctx_union)
    ctx_roads = roads[roads.geometry.length > 0]

    # --- NYC details -------------------------------------------------------------
    mm = hydro.name.fillna("").str.upper().eq("MARSH")
    marsh = unary_union(hydro[mm].geometry.simplify(40)).intersection(nyc_land)
    pond = unary_union(hydro[~mm].geometry.simplify(40)).intersection(nyc_land.buffer(-80))

    parks_z = ["Central Park", "Prospect Park", "Flushing Meadows-Corona Park", "Van Cortlandt Park",
               "Pelham Bay Park", "Bronx Park", "Forest Park/Highland Park", "Highbridge Park",
               "Inwood Hill Park", "Crotona Park", "Astoria Park", "Battery Park", "Freshkills Park",
               "Great Kills Park", "Marine Park/Floyd Bennett Field", "Green-Wood Cemetery",
               "Randalls Island", "Governor's Island/Ellis Island/Liberty Island", "Roosevelt Island",
               "Saint Michaels Cemetery/Woodside", "Baisley Park"]
    parks = smooth(unary_union(taxi[taxi.zone.isin(parks_z)].geometry), 50, 40).intersection(nyc_land.buffer(30))
    airports = smooth(unary_union(taxi[taxi.zone.isin(["JFK Airport", "LaGuardia Airport",
                                                      "Newark Airport"])].geometry), 50, 40)

    cscl["w"] = pd.to_numeric(cscl.st_width, errors="coerce")
    nm = cscl.full_stree.fillna("").str.upper()
    not_path = ~nm.str.contains("GREENWAY|PATH|PEDESTRIAN|BIKE|WALK|PROMENADE|PED ")
    hwy = cscl[cscl.rw_type.isin(["2", "4"]) | ((cscl.rw_type == "3") & not_path)]
    ave = cscl[(cscl.rw_type == "1") & (cscl.w >= 60)]
    street = cscl[(cscl.rw_type == "1") & (cscl.w >= 36) & (cscl.w < 60)]
    local = cscl[(cscl.rw_type == "1") & (cscl.w < 36)]
    ferry = cscl[cscl.rw_type == "14"].copy()
    ferry["geometry"] = ferry.geometry.intersection(nyc_land.buffer(1300))

    return dict(
        nyc_land=nyc_land, ctx_union=ctx_union, ctx_borders=ctx_borders, ctx_urban=ctx_urban,
        ctx_roads=segs(ctx_roads.geometry, 120), marsh=marsh, pond=pond, parks=parks, airports=airports,
        street=segs(street.geometry, 30), local=segs(local.geometry, 30), ave=segs(ave.geometry, 30), hwy=segs(hwy.geometry, 25),
        ferry=segs(ferry.geometry, 60), subway=segs(subl.geometry, 30),
        stations=np.array([(p.x, p.y) for p in subs.geometry]), bounds=nyc_land.bounds)


# ----------------------------------------------------------------------------
# 5. RASTER (matplotlib, antialiasing off)
# ----------------------------------------------------------------------------
class View:
    def __init__(self, bounds):
        minx, miny, maxx, maxy = bounds
        self.w = (maxx - minx) * 1.38
        self.h = self.w * PH / PW
        self.cx, self.cy = (minx + maxx) / 2, (miny + maxy) / 2
        self.x0, self.y1 = self.cx - self.w / 2, self.cy + self.h / 2
        self.mpp = self.w / PW

    def px(self, x, y):
        return (x - self.x0) / self.mpp, (self.y1 - y) / self.mpp

    def lonlat(self, lon, lat):
        p = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(CRS).iloc[0]
        return self.px(p.x, p.y)


def raster(L, V):
    fig = plt.figure(figsize=(PW / 100, PH / 100), dpi=100, facecolor=PAL["w0"])
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.set_facecolor(PAL["w0"])

    def poly(g, face, edge="none", lw=0.0, z=1):
        if g is None or g.is_empty:
            return
        gpd.GeoSeries([g]).plot(ax=ax, facecolor=face, edgecolor=edge, linewidth=lw, antialiased=False,
                                aspect=None, zorder=z)

    def lines(sg, color, px_w=1.0, z=5, style="-"):
        ax.add_collection(LineCollection(sg, colors=color, linewidths=px_w * 0.72, antialiaseds=False,
                                         zorder=z, linestyles=style, capstyle="butt"))

    land, ctx = L["nyc_land"], L["ctx_union"]
    both = unary_union([land, ctx])

    # water: deep -> shallow bands -> foam line (all hard-edged, pixel style)
    poly(both.buffer(2800, join_style=1), PAL["w1"], z=1)
    poly(both.buffer(1400, join_style=1), PAL["w2"], z=1.1)
    poly(both.buffer(200, join_style=1), PAL["w3"], z=1.2)

    # surroundings: washed-out version of the same world
    poly(ctx, PAL["c0"], z=2)
    poly(L["ctx_urban"], PAL["c_urban"], z=2.1)
    lines(segs([L["ctx_borders"]], 40), PAL["c_line"], 1, z=2.2)
    lines(L["ctx_roads"], PAL["c_road"], 1, z=2.3)

    # NYC: shadow, then land with a dark sprite-style outline
    poly(affinity.translate(land, xoff=V.mpp * 2, yoff=-V.mpp * 2), PAL["w0"], z=3)
    parts = list(getattr(land, "geoms", [land]))
    big = unary_union([p for p in parts if p.area > 2.0e6])
    poly(land, PAL["g0"], z=4)
    poly(big, PAL["g0"], PAL["outline"], 1.0, z=4.05)
    poly(L["marsh"], PAL["marsh"], z=4.2)
    poly(L["airports"], PAL["airport"], z=4.3)
    poly(L["parks"], PAL["park"], z=4.4)
    poly(L["pond"], PAL["w2"], z=4.5)

    lines(L["street"], PAL["street"], 1, z=5)
    lines(L["ave"], PAL["avenue"], 1, z=5.2)
    lines(L["hwy"], PAL["hwy_case"], 3, z=5.4)
    lines(L["hwy"], PAL["hwy"], 1, z=5.5)
    lines(L["ferry"], PAL["w3"], 1, z=5.6, style=(0, (2, 2)))
    lines(L["subway"], PAL["subway"], 1, z=6)
    # re-stroke the coastline outline so roads never cover it
    poly(big, "none", PAL["outline"], 1.0, z=6.5)

    ax.set_xlim(V.x0, V.x0 + V.w); ax.set_ylim(V.y1 - V.h, V.y1); ax.set_aspect("auto")
    fig.canvas.draw()
    arr = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    plt.close(fig)
    assert arr.shape[:2] == (PH, PW), arr.shape
    return arr


def mask_raster(sg, V):
    """1px lines on black -> boolean mask (used to measure street density)."""
    fig = plt.figure(figsize=(PW / 100, PH / 100), dpi=100, facecolor="black")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.add_collection(LineCollection(sg, colors="white", linewidths=0.72, antialiaseds=False))
    ax.set_xlim(V.x0, V.x0 + V.w); ax.set_ylim(V.y1 - V.h, V.y1)
    fig.canvas.draw()
    m = np.asarray(fig.canvas.buffer_rgba())[:, :, 0] > 127
    plt.close(fig)
    return m


def box_mean(m, r):
    a = np.pad(m.astype(np.float32), r, mode="edge")
    c = np.cumsum(np.cumsum(a, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    k = 2 * r + 1
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def town(arr, local_mask):
    """dense street grid -> cobbled 'town' ground; medium density -> checker dither with grass."""
    dens = box_mean(local_mask, 3)
    grass = is_col(arr, C["g0"]) | is_col(arr, C["g1"]) | is_col(arr, C["g2"])
    yy, xx = np.mgrid[0:PH, 0:PW]
    checker = (xx + yy) % 2 == 0
    arr[grass & (dens > 0.50)] = C["town"]
    arr[grass & (dens > 0.26) & (dens <= 0.50) & checker] = C["town"]


# ----------------------------------------------------------------------------
# 6. PIXEL FX
# ----------------------------------------------------------------------------
def snap_to_palette(arr):
    """Any stray blended pixel is moved to the nearest palette colour."""
    pal = np.array(list(C.values()), dtype=np.int32)
    flat = arr.reshape(-1, 3).astype(np.int32)
    exact = (flat[:, None, :] == pal[None]).all(2).any(1)
    bad = np.where(~exact)[0]
    if len(bad):
        d = ((flat[bad][:, None, :] - pal[None]) ** 2).sum(2)
        flat[bad] = pal[d.argmin(1)]
    print(f"  snapped {len(bad)} stray pixels of {len(flat)}")
    return flat.reshape(arr.shape).astype(np.uint8)


def is_col(arr, c):
    return (arr == np.array(c, dtype=np.uint8)).all(2)


def tufts(arr, base, c1, c2, p1=0.05, p2=0.025):
    m = is_col(arr, base)
    pair = m & np.roll(m, -1, axis=1)
    r = rng.random(m.shape)
    a, b = pair & (r < p1), pair & (r >= p1) & (r < p1 + p2)
    for mask, col in ((a, c1), (b, c2)):
        arr[mask] = col
        arr[np.roll(mask, 1, axis=1)] = col


def sparkle(arr):
    for base, light, p in ((C["w0"], C["w1"], 0.004), (C["w1"], C["w2"], 0.004), (C["w2"], C["w3"], 0.003)):
        m = is_col(arr, base)
        ok = m & np.roll(m, -1, 1) & np.roll(m, -2, 1) & (rng.random(m.shape) < p)
        for k in (0, 1, 2):
            arr[np.roll(ok, k, axis=1)] = light


def trees(arr):
    park = is_col(arr, C["park"])
    for y in range(2, PH - 3, 4):
        for x in range(2, PW - 3, 4):
            yy, xx = y + rng.integers(-1, 2), x + rng.integers(-1, 2)
            if rng.random() < 0.7 and park[yy - 1:yy + 2, xx - 1:xx + 2].all():
                arr[yy - 1:yy + 2, xx - 1:xx + 2] = C["tree_d"]
                arr[yy - 1, xx - 1] = C["tree_l"]; arr[yy - 1, xx] = C["tree_l"]


def stations(arr, V, pts):
    for x, y in pts:
        px, py = V.px(x, y)
        px, py = int(round(px)), int(round(py))
        if 0 <= px < PW and 0 <= py < PH:
            arr[py, px] = C["station"]


PIN = ["..kkkkk..", ".krrrrrk.", "krrcccrrk", "krrcccrrk", "krrrrrrrk", ".krrrrrk.", "..krrrk..", "...krk...", "....k...."]
PINC = {"k": C["outline"], "r": C["red"], "c": C["cream"]}


def pin(arr, px, py):
    px, py = int(round(px)), int(round(py))
    for j, row in enumerate(PIN):
        for i, ch in enumerate(row):
            if ch != ".":
                y, x = py - 8 + j, px - 4 + i
                if 0 <= y < PH and 0 <= x < PW:
                    arr[y, x] = PINC[ch]


# ----------------------------------------------------------------------------
# 7. UI: pixel fonts, panels, labels
# ----------------------------------------------------------------------------
class UI:
    def __init__(self, arr):
        self.img = Image.fromarray(arr)
        self.d = ImageDraw.Draw(self.img); self.d.fontmode = "1"
        self.f = {}

    def font(self, name, size):
        k = (name, size)
        if k not in self.f:
            self.f[k] = ImageFont.truetype(os.path.join(FONTS, name), size)
        return self.f[k]

    def text(self, xy, s, name="Silkscreen-Regular.ttf", size=8, fill="ink", outline=None, anchor="la",
             shadow=None, spacing=2):
        f = self.font(name, size)
        x, y = xy
        if outline:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx or dy:
                        self.d.multiline_text((x + dx, y + dy), s, font=f, fill=C[outline], anchor=anchor,
                                              spacing=spacing, align="center")
        if shadow:
            self.d.multiline_text((x + 1, y + 1), s, font=f, fill=C[shadow], anchor=anchor, spacing=spacing,
                                  align="center")
        self.d.multiline_text((x, y), s, font=f, fill=C[fill], anchor=anchor, spacing=spacing, align="center")

    def vtext(self, xy, s, size=8, fill="ink", outline=None):
        """text rotated exactly 90deg (keeps pixels crisp), centred on xy."""
        f = self.font("Silkscreen-Regular.ttf", size)
        w = int(self.d.textlength(s, font=f)) + 4
        layer = Image.new("RGBA", (w, size + 4), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer); ld.fontmode = "1"
        if outline:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    ld.text((2 + dx, 2 + dy), s, font=f, fill=C[outline])
        ld.text((2, 2), s, font=f, fill=C[fill])
        layer = layer.rotate(90, expand=True)
        self.img.paste(layer, (int(xy[0] - layer.width / 2), int(xy[1] - layer.height / 2)), layer)

    def panel(self, x0, y0, x1, y1):
        d = self.d
        d.rectangle([x0, y0, x1, y1], fill=C["ink"])
        d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=C["wood"])
        d.rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], fill=C["wood_d"])
        d.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill=C["parch"])
        d.line([(x0 + 4, y1 - 4), (x1 - 4, y1 - 4)], fill=C["parch_d"])
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):   # notch the corners
            d.point((cx, cy), fill=C["w0"])


LANDMARKS = [  # name, lon, lat, side
    ("Empire State", -73.9857, 40.7484, "l"), ("One WTC", -74.0134, 40.7127, "l"),
    ("Statue of Liberty", -74.0445, 40.6892, "l"), ("Brooklyn Bridge", -73.9969, 40.7061, "r"),
    ("Central Park", -73.9654, 40.7829, "r"), ("Yankee Stadium", -73.9262, 40.8296, "r"),
    ("Citi Field", -73.8458, 40.7571, "r"), ("Coney Island", -73.9786, 40.5750, "b"),
    ("Verrazzano Br.", -74.0447, 40.6066, "l"), ("Bronx Zoo", -73.8770, 40.8506, "r"),
    ("St George Ferry", -74.0737, 40.6437, "l"),
]


def river_center_x(arr, y0, y1, x0, x1):
    """x of the river's centre line, measured from the water pixels actually drawn."""
    water = sum(is_col(arr, C[k]) for k in ("w0", "w1", "w2", "w3")).astype(bool)
    mids = []
    for row in water[y0:y1, x0:x1]:
        xs = np.nonzero(row)[0]
        if len(xs):
            mids.append((xs.min() + xs.max()) / 2)     # midpoint between the two banks
    return x0 + float(np.mean(mids))


def ui_layer(arr, V, hudson=True):
    P = lambda lon, lat: V.lonlat(lon, lat)
    hud_x = river_center_x(arr, 4, 84, 400, 560) if hudson else None
    for name, lon, lat, side in LANDMARKS:
        pin(arr, *P(lon, lat))
    ui = UI(arr)

    # context names (faded) + water names
    for t, lon, lat in [("NEW JERSEY", -74.19, 40.80), ("NASSAU", -73.665, 40.735), ("WESTCHESTER", -73.82, 41.02)]:
        ui.text(P(lon, lat), t, size=8, fill="c_text", outline="c0", anchor="mm")
    for t, lon, lat in [("UPPER BAY", -74.045, 40.668), ("LOWER BAY", -74.08, 40.53),
                        ("ATLANTIC OCEAN", -73.90, 40.47), ("JAMAICA BAY", -73.842, 40.612),
                        ("LONG ISLAND SOUND", -73.70, 40.90)]:
        ui.text(P(lon, lat), t, size=8, fill="cream", outline="w0", anchor="mm")
    if hudson:
        ui.vtext((hud_x, 44), "HUDSON RIVER", fill="cream", outline="w0")

    # borough names
    for t, lon, lat, sz in [("BRONX", -73.866, 40.863, 16), ("QUEENS", -73.800, 40.703, 16),
                            ("BROOKLYN", -73.947, 40.640, 16), ("STATEN\nISLAND", -74.150, 40.575, 16)]:
        ui.text(P(lon, lat), t, size=sz, fill="ink", outline="parch", anchor="mm")
    ui.vtext(P(-73.955, 40.805), "MANHATTAN", size=8, fill="ink", outline="parch")
    for t, lon, lat in [("JFK", -73.779, 40.641), ("LGA", -73.874, 40.777), ("EWR", -74.1745, 40.6895)]:
        ui.text(P(lon, lat), t, size=8, fill="ink", anchor="mm")

    # landmarks: sprite + label
    for name, lon, lat, side in LANDMARKS:
        x, y = P(lon, lat)
        s = name.upper()
        if side == "r":
            ui.text((x + 7, y - 5), s, fill="cream", outline="ink", anchor="lm")
        elif side == "l":
            ui.text((x - 7, y - 5), s, fill="cream", outline="ink", anchor="rm")
        else:
            ui.text((x, y + 6), s, fill="cream", outline="ink", anchor="mt")

    # title panel
    ui.panel(12, 12, 322, 120)
    ui.text((26, 24), "NEW YORK", size=32, fill="ink", shadow="wood")
    ui.text((26, 66), "a pixel-art map, built from code", "VT323-Regular.ttf", 18, fill="wood_d")
    ui.text((26, 84), "from real open geodata", "VT323-Regular.ttf", 18, fill="wood_d")
    ui.text((26, 102), "#30DayMapChallenge", size=8, fill="subway")

    # legend panel
    lx, ly = 12, 128
    ui.panel(lx, ly, lx + 128, ly + 154)
    ui.text((lx + 12, ly + 10), "LEGEND", size=8, fill="ink")
    d = ui.d
    rows = [("PARK", "park"), ("STREET", "street"), ("AVENUE", "avenue"), ("HIGHWAY", "hwy"),
            ("SUBWAY", "subway"), ("AIRPORT", "airport"), ("MARSH", "marsh"), ("LANDMARK", None),
            ("OUTSIDE NYC", "c0")]
    for i, (lab, key) in enumerate(rows):
        y = ly + 24 + i * 14
        sx = lx + 12
        if key in ("street", "avenue", "subway"):
            d.rectangle([sx, y + 3, sx + 15, y + 4], fill=C[key])
        elif key == "hwy":
            d.rectangle([sx, y + 2, sx + 15, y + 5], fill=C["hwy_case"]); d.rectangle([sx, y + 3, sx + 15, y + 4], fill=C["hwy"])
        elif key is None:
            for j, row in enumerate(PIN[:-1]):
                for k, ch in enumerate(row):
                    if ch != ".":
                        d.point((sx + 3 + k - 1, y - 2 + j), fill=PINC[ch])
        else:
            d.rectangle([sx, y, sx + 15, y + 7], fill=C[key], outline=C["outline"])
        ui.text((sx + 22, y + 4), lab, size=8, fill="ink", anchor="lm")

    # scale bar + north arrow
    sw = 5000 / V.mpp
    bx0, by = PW - 12 - (sw + 24 + 44), PH - 94
    ui.panel(int(bx0), by, PW - 12, by + 46)
    x0 = int(bx0 + 12)
    for i in range(5):
        d.rectangle([x0 + int(i * sw / 5), by + 14, x0 + int((i + 1) * sw / 5), by + 20],
                    fill=C["ink"] if i % 2 == 0 else C["cream"], outline=C["ink"])
    ui.text((x0, by + 24), "0", size=8, fill="ink"); ui.text((x0 + int(sw) - 12, by + 24), "5 KM", size=8, fill="ink")
    ax_ = PW - 12 - 22
    d.polygon([(ax_, by + 8), (ax_ - 5, by + 22), (ax_ + 5, by + 22)], fill=C["red"], outline=C["ink"])
    ui.text((ax_, by + 26), "N", size=8, fill="ink", anchor="ma")

    # sources strip
    ui.panel(12, PH - 44, PW - 12, PH - 8)
    ui.text((22, PH - 35), "DATA: NYC OPEN DATA (BOROUGHS, STREETS, WATER, SUBWAY, TLC ZONES) + NATURAL EARTH", size=8, fill="wood_d")
    ui.text((22, PH - 23), "CODE: PYTHON, GEOPANDAS, MATPLOTLIB  |  UTM 18N  |  1 PIXEL = 81 M  |  NO IMAGE GENERATOR", size=8, fill="wood_d")
    return np.asarray(ui.img)


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    fetch()
    L = build()
    V = View(L["bounds"])
    print(f"1 pixel = {V.mpp:.1f} m")
    arr = raster(L, V)
    arr = snap_to_palette(arr)
    tufts(arr, C["g0"], C["g1"], C["g2"])
    tufts(arr, C["c0"], C["c1"], C["c2"], 0.05, 0.03)
    town(arr, mask_raster(L["local"], V))
    sparkle(arr)
    trees(arr)
    stations(arr, V, L["stations"])
    base = arr
    for hudson, out in ((True, OUT), (False, OUT.replace(".png", "_no_hudson.png"))):
        a = snap_to_palette(ui_layer(base.copy(), V, hudson).copy())
        img = Image.fromarray(a)
        if hudson:
            img.save(OUT_SMALL)
        img.resize((PW * SCALE, PH * SCALE), Image.NEAREST).save(out, optimize=True)
        print("colours used:", len(np.unique(a.reshape(-1, 3), axis=0)), "| saved", out)
