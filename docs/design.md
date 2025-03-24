# 2D Portals Game Design Document

---

## 1. **Game Layout**

### 1.1 **Main Game Area**
- **Dimensions:** 1280x720 pixels (16:9 aspect ratio).
- **Background:** A dynamic background that changes based on the selected theme (e.g., dark space, light grid, or abstract patterns).
- **Boundaries:** Visible walls on all sides to contain objects, with a subtle glow effect to indicate boundaries.

### 1.2 **HUD (Heads-Up Display)**
- **Position:** Top-left corner.
- **Elements:**
  - FPS counter.
  - Object count.
  - Portal count.
  - Gravity status (ON/OFF).
  - Current theme name.
- **Style:** Minimalistic with a semi-transparent background.

---

## 2. **Objects**

### 2.1 **Types of Objects**
- **Boxes:**
  - Shape: Rectangular.
  - Default Size: 32x32 pixels.
  - Colors: Theme-dependent (e.g., light gray in dark mode, dark blue in light mode).
  - Interactions: Can be dragged, thrown, resized, and rotated.
- **Circles:**
  - Shape: Circular.
  - Default Radius: 16 pixels.
  - Colors: Bright and vibrant (e.g., yellow or orange).
  - Interactions: Same as boxes.
- **Triangles:**
  - Shape: Equilateral triangle.
  - Default Size: 32 pixels per side.
  - Colors: Theme-dependent (e.g., cyan or magenta).
  - Interactions: Same as boxes and circles.
- **Custom Shapes:**
  - Future additions like polygons or irregular shapes for variety.

### 2.2 **Physics**
- **Gravity:** Affects all objects unless toggled off.
- **Collisions:** Realistic interactions between objects and portals.
- **Momentum:** Objects retain momentum when thrown or teleported.

---

## 3. **Portals**

### 3.1 **Appearance**
- **Shape:** Rectangular with rounded edges.
- **Size:** Default size is 10x50 pixels, adjustable by the player.
- **Colors:** Unique for each pair (e.g., blue/orange, green/purple).
- **Effects:**
  - Glow effect around the edges.
  - Subtle particle effects when active.
  - A small indicator (e.g., an arrow) to show the exit direction.

### 3.2 **Directional Indicators**
- **Purpose:** Show the direction an object will exit after teleportation.
- **Design:**
  - A small arrow or chevron at the portal's edge pointing outward.
  - Arrow color matches the portal's color.
  - Animates briefly when an object enters the portal.

### 3.3 **Animations**
- **Disappearing Objects:**
  - Objects shrink and fade out as they enter the portal.
  - A swirl or ripple effect around the portal.
- **Reappearing Objects:**
  - Objects grow and fade in as they exit the linked portal.
  - A burst of particles around the portal.

### 3.4 **Behavior**
- **Teleportation:**
  - Objects entering one portal exit through the linked portal.
  - Momentum and orientation are preserved.
- **Placement Rules:**
  - Can only be placed on valid surfaces.
  - Overlapping portals are automatically adjusted.
- **Cooldown:**
  - Objects cannot pass through portals of the same color for a specific cooldown period.

---

## 4. **User Interface**

### 4.1 **Main Menu**
- **Elements:**
  - Start Game button.
  - Settings button.
  - Exit button.
- **Style:** Centered menu with large, rounded buttons and hover effects.

### 4.2 **In-Game Menu**
- **Access:** Opened via a menu icon in the top-right corner.
- **Options:**
  - Toggle themes.
  - View controls/help.
  - Exit to main menu.
- **Style:** Semi-transparent background with a clean layout.

### 4.3 **Context Menu**
- **Access:** Right-click on an object or portal.
- **Options:**
  - Resize (increase/decrease size).
  - Rotate (clockwise/counterclockwise).
  - Delete.
- **Style:** Compact menu with hover highlights.

### 4.4 **Sliders for Adjustments**
- **Purpose:** Provide precise control over size and rotation.
- **Design:**
  - Sliders for size (scale from 0.5x to 2.0x).
  - Sliders for rotation (0° to 360°).
  - Real-time preview as the slider is adjusted.

---

## 5. **Colors and Themes**

### 5.1 **Themes**
- **Dark Theme:**
  - Background: Deep blue with subtle stars.
  - Object Colors: Light gray boxes, bright yellow circles.
  - Portal Colors: Vibrant blue/orange.
- **Light Theme:**
  - Background: Light gray grid.
  - Object Colors: Dark blue boxes, muted yellow circles.
  - Portal Colors: Soft green/purple.
- **Dusk Theme:**
  - Background: Gradient from purple to orange.
  - Object Colors: Light blue boxes, soft orange circles.
  - Portal Colors: Cyan/magenta.
- **Cream Theme:**
  - Background: Warm beige with subtle textures.
  - Object Colors: Brown boxes, dark orange circles.
  - Portal Colors: Yellow/teal.

### 5.2 **Dynamic Adjustments**
- **Tinting:** Objects and portals adjust brightness based on the theme.
- **Transitions:** Smooth fade effects when switching themes.

---

## 6. **Visual Effects**

### 6.1 **Portal Effects**
- **Glow:** Dynamic glow around active portals.
- **Particles:** Small particles flow into the portal, indicating activity.
- **Link Indicator:** A subtle line or animation between linked portals.
- **Directional Arrows:** Show the exit direction of linked portals.

### 6.2 **Object Effects**
- **Dragging:** Slight shadow and scaling effect when an object is grabbed.
- **Throwing:** Motion blur effect for fast-moving objects.
- **Teleportation:** Shrinking and fading out/in animations.

### 6.3 **Background Effects**
- **Dynamic Backgrounds:** Subtle animations like moving stars or shifting gradients.
- **Theme-Specific Details:** E.g., grid lines in light mode, stars in dark mode.

---

## 7. **Audio Design**

### 7.1 **Sound Effects**
- **Portal Activation:** A soft "whoosh" sound.
- **Object Collisions:** Subtle thuds or clinks.
- **Dragging/Throwing:** Gentle scraping or air-rush sounds.
- **Teleportation:** A fading "zap" sound as objects disappear and reappear.

### 7.2 **Background Music**
- **Themes:**
  - Dark: Ambient space music.
  - Light: Calm piano melodies.
  - Dusk: Soft synthwave.
  - Cream: Relaxing acoustic tunes.
- **Volume Control:** Adjustable in settings.

---

## 8. **Player Experience**

### 8.1 **Accessibility**
- **Adjustable Difficulty:** Options to tweak gravity, object speed, and cooldown times.

### 8.2 **Replayability**
- **Sandbox Mode:** Unlimited objects and portals for creative experimentation.
- **Challenges:** Timed puzzles or objectives to complete.

### 8.3 **Feedback**
- **Visual Cues:** Highlight objects and portals when interacted with.
- **Audio Cues:** Subtle sounds for actions like teleportation or collisions.

---