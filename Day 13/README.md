# Shibuya Crossing Simulator

An agent-based model (ABM) of pedestrians crossing Shibuya Crossing in Tokyo, built in Unity with Google's photorealistic 3D tiles streamed through Cesium. Made for Day 13 ("Interactions") of #30DayMapChallenge 2026.

A crowd spawns at the corners of the scramble crossing, waits a moment, then everyone crosses to a different corner at once. Two variables drive the experiment:

- **Crowd size**: how many people are waiting at the lights
- **Aggressive share**: the fraction of pedestrians who walk faster, keep less personal space, give way less and step off sooner

Blue capsules are polite pedestrians and red capsules are aggressive ones. A run ends when everyone has crossed. Press **Reset** to run again with new settings.

**Play it in the browser:** https://jamestansongen.itch.io/shibuya-crossing-simulator (best in Chrome or Edge on desktop)

---

## Contents

1. [How the model works](#how-the-model-works)
2. [Requirements](#requirements)
3. [Scripts in this repo](#scripts-in-this-repo)
4. [Setup in Unity](#setup-in-unity)
5. [Building for the web and publishing on itch.io](#building-for-the-web-and-publishing-on-itchio)
6. [Troubleshooting](#troubleshooting)
7. [Credits and licences](#credits-and-licences)

---

## How the model works

Each pedestrian follows a **social force model** (Helbing and Molnár): they are pulled towards their goal at their preferred speed, pushed away from nearby people, and pushed away from optional walls or kerbs. On top of that:

- **Anisotropy:** people react more to those in front than behind
- **Lane following:** polite walkers drift into the flow of people heading the same way
- **Keep left:** polite walkers sidestep head-on walkers to the left, as people tend to in Tokyo
- **Jostle:** a small random force breaks perfectly balanced stand-offs
- **Arrival:** a crosser has arrived once they reach the crowd standing at their destination corner. The arrival zone grows as people pile up, and people already standing there make way for latecomers.

The simulation runs at a fixed 25 steps per second, independent of frame rate, and uses a spatial hash grid for neighbour lookups. People are drawn with GPU instancing, so thousands of capsules render cheaply.

Each finished run is appended to `crossing_log.csv` in `Application.persistentDataPath` (the Console prints the path), with crowd size, aggressive share, time to clear, bump count and average crossing time for polite and aggressive pedestrians.

---

## Requirements

| Item | Version or notes |
|---|---|
| Unity | **6.3 LTS** (6000.3.x) with the **Universal 3D (URP)** template. Add **Web Build Support** in Unity Hub if you want a web build. |
| Cesium for Unity | **1.20.0 or newer** (needed for web builds) |
| Cesium ion account | Free Community account at [ion.cesium.com](https://ion.cesium.com), for non-commercial use |
| Traffic light models | [City Traffic Lights Pack [FREE] - Low Poly 3D Art](https://assetstore.unity.com/) by Tarbo Studios (Unity Asset Store). Any light model works; they're only visual markers. |
| TextMeshPro | Included with Unity. Import **TMP Essentials** when prompted. |

**Keep the Unity project outside Dropbox, OneDrive or Google Drive.** Sync clients lock files while Unity builds and cause build-system errors.

---

## Scripts in this repo

| Script | Purpose |
|---|---|
| `CrowdSim.cs` | The simulation: spawning, social force model, arrivals, run control, rendering and logging |
| `CrowdUI.cs` | Connects the sliders and buttons to `CrowdSim` and shows live stats |
| `CornerZone.cs` | A waiting area at a corner. People spawn in one and cross to another. |
| `WallPolyline.cs` | Optional kerb or barrier that people are pushed away from (child transforms are the vertices) |

Copy them into `Assets/Scripts/`.

---

## Setup in Unity

### 1. Install Cesium for Unity

1. **Edit → Project Settings → Package Manager**, then add a scoped registry:
   - Name: `Cesium`
   - URL: `https://unity.pkg.cesium.com`
   - Scope: `com.cesium.unity`
2. **Window → Package Manager → My Registries → Cesium for Unity → Install**.
3. Open the **Cesium** panel, click **Connect to Cesium ion**, and create a default project token when asked.

### 2. Add Shibuya

1. In the Cesium panel under **Quick Add Cesium ion Assets**, add **Google Photorealistic 3D Tiles**.
2. If **Cesium OSM Buildings** was added too, disable it. Google's tiles already include buildings.
3. If the Console shows `Could not access Cesium ion asset`, remove any **Cesium Ion Raster Overlay** component from the tileset. Google's tiles carry their own textures.
4. Select **CesiumGeoreference** and set:

   | Field | Value |
   |---|---|
   | Origin Authority | Longitude Latitude Height |
   | Latitude | 35.6595 |
   | Longitude | 139.7005 |
   | Height | about **52** (see below) |

   Leave the georeference's **Transform** at 0, 0, 0. All positioning happens through these fields.

5. **Set the height so the road sits at Y = 0.** The scripts assume the ground is at Y = 0. The Height field is an absolute altitude above the ellipsoid, not an offset: it says which real-world altitude becomes Unity's zero.
   - Place a Cube at (0, 0, 0) and move it up until its bottom touches the road. Note how much you moved it.
   - Add that amount to the current Height. For example, if Height was 50 and the road was 2 m above the grid, set Height to 52. Raising Height moves the city down.
   - Delete the cube.
6. Optional, for sharper tiles: select **Google Photorealistic 3D Tiles** and lower **Maximum Screen Space Error** from 16 to about 8.

### 3. Camera

Select **Main Camera** and set:

| Setting | Value |
|---|---|
| Position | 0, 50, -50 |
| Rotation | 45, 0, 0 |
| Clipping Planes | Near **1**, Far **5000** |

Use (0, 120, -120) for a wider overview, or (0, 25, -35) with rotation (35, 0, 0) for a closer, livecam-style view. Going much lower than 25 m shows the limits of the photo mesh.

### 4. Traffic lights and waiting areas

1. Import the traffic light pack from **Window → Package Manager → My Assets**.
2. If the models are pink, open **Window → Rendering → Render Pipeline Converter**, choose **Built-in to URP**, tick **Material Upgrade** and click **Initialize And Convert**.
3. Create an empty **Markers** object. Drag a traffic light prefab to each corner of the scramble, under Markers, at Y = 0.
4. Under **one light per corner** (Shibuya has five corners), right-click → **Create Empty**, name it **WaitArea**, and add **CornerZone**:

   | Field | Value |
   |---|---|
   | Radius | 5–8 (shown as a green gizmo circle) |
   | Weight | **3** for the station / Hachikō corner, **1** for the others |

5. Move each WaitArea onto the pavement **behind** its light, so the circle sits mostly off the road. Check from a top-down view.

```
Markers
├── TrafficLight (1)
│   └── WaitArea      ← CornerZone
├── TrafficLight (2)
│   └── WaitArea      ← CornerZone
└── ...
```

### 5. Pedestrian materials

Create two materials, **Polite** (blue) and **Aggressive** (red):

- Shader: **Universal Render Pipeline/Lit**
- **Enable GPU Instancing**: ticked. **This is required. Without it, nobody appears.**

### 6. CrowdSim

Create an empty **CrowdSim** object, add the **CrowdSim** component, and set:

| Field | Value |
|---|---|
| Markers | All five WaitAreas |
| World Bounds | (-100, -100, 200, 200) |
| Ground Y | 0 |
| Agent Mesh | **Capsule** (click ⊙ and search "Capsule") |
| Polite / Aggressive Material | The two materials above |
| Agent Height / Diameter | 1.7 / 0.5 |
| Character Prefabs | Leave empty for capsules |
| Run On Start | Ticked |
| Start Delay | 2 s |

Press **Play**. A crowd spawns, waits 2 seconds, and crosses.

**Behaviour parameters.** The **Polite (x) → aggressive (y)** section has two values per behaviour: X for polite people, Y for aggressive people. The defaults are mild. For clearly pushier aggressive pedestrians, use:

| Field | Polite (X) | Aggressive (Y) | Effect |
|---|---|---|---|
| Desired Speed | 1.3 | 2.0 | Walking speed, m/s |
| Personal Space | 0.2 | 0 | Extra gap kept around the body, m |
| Repulsion Strength | 2.0 | 0.6 | How strongly others push them away |
| Repulsion Range | 0.3 | 0.15 | How early they react to people in the way |
| Lane Following | 0.6 | 0 | Joins the flow of people going the same way |
| Keep Left | 0.5 | 0 | Sidesteps head-on walkers |
| Rear Awareness | 0.5 | 0.15 | Notices people beside and behind |
| Reaction Time | 1.2 | 0.1 | Max delay before stepping off, s |

**Arrival settings**, rarely needed:

| Field | Default | Notes |
|---|---|---|
| Area Per Person | 0.5 m² | How fast the arrival zone grows as people pile up |
| Stuck Arrival Time | 6 s | Someone pinned near their corner this long counts as arrived |
| Standing Crowd Softness | 0.2 | How much arrived people resist crossers (0–1). Raise it if crossers pass through standing crowds too easily. |
| Max Duration | 300 s | Safety cutoff for gridlock |

Inspector changes made during Play mode are lost when you stop. To keep them, right-click the component header → **Copy Component**, stop Play, then **Paste Component Values**.

### 7. UI

1. **GameObject → UI → Canvas**. On the Canvas Scaler, set **Scale With Screen Size** at **1920 × 1080**, with Match **0.5**.
2. Right-click Canvas → **UI → Panel**, and name it **ControlPanel**.
   - In Rect Transform, click the anchor preset square, hold **Shift + Alt**, and click **top-left**. Then set Pos X **20**, Pos Y **-20**, Width **380**, Height **460**.
   - Set the Image colour to black with alpha about 160.
   - Add a **Vertical Layout Group** with padding 16, spacing 8, **Control Child Size: Width ✓, Height ✗**, and **Child Force Expand: Width ✓, Height ✗**.
3. Add these children in order:

   | Name | Type | Settings |
   |---|---|---|
   | CrowdLabel | Text - TextMeshPro | Font size 22, white, height 30 |
   | CrowdSlider | Slider | Height 20 |
   | AggressionLabel | Text - TextMeshPro | Same as CrowdLabel |
   | AggressionSlider | Slider | Height 20 |
   | SpeedLabel | Text - TextMeshPro | Same as CrowdLabel |
   | SpeedSlider | Slider | Height 20 |
   | ResetButton | Button - TextMeshPro | Height 40. Set the child text's **Text Input** to "Reset". |
   | GoButton (optional) | Button - TextMeshPro | Height 40, "Go". Skips the start delay. |
   | StatsText | Text - TextMeshPro | Font size 18, white, height 150 |

4. Add **CrowdUI** to ControlPanel and drag in the CrowdSim object, the three sliders, the button(s), the three labels and StatsText.

Labels and slider ranges are filled in by the script at runtime, so they show "New Text" until you press Play. Crowd size and aggressive share apply on the next **Reset**; sim speed applies immediately.

The Canvas appears as a huge sheet in the Scene view, because UI is drawn at 1 pixel = 1 unit. That's normal; check the UI in the Game view.

### 8. Optional: character models instead of capsules

Drag humanoid prefabs into **Character Prefabs** on CrowdSim, for example the free *npc_casual_set_00* pack from the Asset Store. Each person gets a random model that slides and turns to face its walking direction (no walk animation). Set **Max Characters** to around 300; anyone beyond that is drawn as a capsule. Set **Marker Mesh** to **Cylinder** to draw a blue or red disc under each character's feet. Models in a T-pose look odd sliding around, so give them an Animator with a single idle clip if needed.

---

## Building for the web and publishing on itch.io

Cesium's web support is labelled experimental, so test in Chrome first and keep crowd sizes modest.

### 1. Player settings

1. **File → Build Profiles → Web → Switch Platform**, and make sure your scene is in the Scene List.
2. In **Player Settings → Web**:

   | Setting | Value |
   |---|---|
   | Default canvas | 1280 × 720 |
   | **Native C/C++ Multithreading** | **Ticked.** Required by Cesium; without it the build fails with `wasm-ld: undefined symbol: __wasm_lpad_context`. |
   | Compression Format | Gzip |
   | Decompression Fallback | Ticked |

### 2. A separate public token

The build streams tiles through a Cesium ion token, and anyone can extract it. Make a separate, restricted token for builds rather than using your own.

1. At [ion.cesium.com](https://ion.cesium.com) → **Access Tokens → Create token**:
   - **Public scopes:** only `assets:read`. Leave every private scope off.
   - **Resources:** Selected assets, with only **Google Photorealistic 3D Tiles** (asset 2275207).
   - **Expiration:** choose one, for example 1 month. The tiles stop loading in the build after that.
   - **Allowed URLs:** Selected Urls, with `https://html.itch.zone`. That's the domain itch.io serves browser games from, and this setting blocks use of the token on other websites. Domains for other hosts can be found in the browser's DevTools under **Network**, in a request to `api.cesium.com` → **Request Headers → Origin**.
2. **Saving changes to a token's Allowed URLs regenerates the token string.** The old string stops working (requests return `401 Unauthorized`), so settle the URLs before copying the token into Unity.
3. Select **Google Photorealistic 3D Tiles** and paste the public token into its **ion Access Token** field. This overrides the project default token for this tileset only. Don't use **Use as Project Default Token** for it: if the public token expires or is revoked, your own project stops loading tiles too.
4. A URL-locked token doesn't work in the Unity editor, because the editor's requests don't come from `html.itch.zone`. So the tiles disappear in the editor while the public token is in the field. Paste it in just before building, then clear the field afterwards to get the tiles back in the editor.

### 3. Build and upload

1. **Build** to an empty folder outside any synced drive. The result should contain `index.html`, `Build/` and `TemplateData/`.
2. Zip the **contents** of that folder, with `index.html` at the top level of the zip.
3. On itch.io, create a new project:
   - **Kind of project:** HTML
   - Upload the zip, then tick **This file will be played in the browser** and **Hide this file and prevent it from being downloaded**
   - **Embed options:** viewport 1280 × 720, **Fullscreen button** ticked, **SharedArrayBuffer support** ticked (required for multithreading)
   - Keep visibility as **Draft** while testing, then switch to **Public**
4. After uploading a new build, reload with **Ctrl+Shift+R** to avoid the cached version.

Double-clicking `index.html` on your computer won't work. Use **Build and Run** in Unity to test locally; it starts a server with the right headers.

---

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `Internal build system error … BuildFinishedMessage` | Unity's `bee_backend` got stuck, usually because a sync client locked files. Close Unity, end `bee_backend.exe` in Task Manager, delete `Library/Bee` and `Temp`, and move the project out of Dropbox or OneDrive. |
| Nobody appears | **Enable GPU Instancing** isn't ticked on the materials, or Agent Mesh is empty |
| Traffic lights are pink | Run the Render Pipeline Converter (Built-in to URP, Material Upgrade) |
| People float or sink | Adjust CesiumGeoreference **Height**: raising it lowers the city |
| Tiles show a forest, not Tokyo | The georeference origin isn't set. Check Origin Authority, latitude and longitude. |
| `Could not access Cesium ion asset` | A raster overlay your token can't access. Remove it from the tileset. |
| Run never finishes | Fixed in the current `CrowdSim.cs` by the growing arrival zone. If it still happens, raise **Standing Crowd Softness** or lower **Stuck Arrival Time**. |
| Web build fails with `__wasm_lpad_context` / `_Unwind_CallPersonality` | Tick **Native C/C++ Multithreading** in Player Settings, and use Cesium for Unity 1.20.0+ |
| "Your browser does not support multithreading" | The page isn't cross-origin isolated. On itch.io tick **SharedArrayBuffer support**; locally, use Build and Run. |
| Tiles don't load in the web build (401 in DevTools) | The token was regenerated, expired or URL-restricted to a different domain. Copy the current token into the tileset's **ion Access Token** field and rebuild. |
| Tiles vanish in the editor after setting up the build token | The URL-locked public token is still in the tileset's **ion Access Token** field. Clear the field to go back to your project default token. |
| `connection.state_change … Bus validation failed` | Comes from the Unity AI Assistant package, not this project. Ignore it or remove that package. |

---

## Credits and licences

- **3D tiles:** Google Photorealistic 3D Tiles via Cesium ion. Keep the on-screen Google and Cesium credits visible in builds and videos. The Cesium ion Community plan is for non-commercial use.
- **Cesium for Unity** by Cesium.
- **Traffic lights:** City Traffic Lights Pack [FREE] by Tarbo Studios, under the Unity Asset Store EULA. **Asset Store content isn't included in this repo and can't be redistributed**; download it from the Asset Store yourself.
- **Pedestrian model:** based on the social force model by Helbing and Molnár (1995), "Social force model for pedestrian dynamics", *Physical Review E* 51(5).

**This repo contains no Cesium tokens.** Use your own Cesium ion account and token.
