# Portals2D Design Document

## UI Design Philosophy
Portals2D will adopt a minimalist, elegant aesthetic inspired by Mini Metro's acclaimed design language. The interface will prioritize:

- **Clean geometric shapes** with minimal visual noise
- **Fluid animations** for all transitions and interactions
- **Limited color palette** with high contrast for gameplay elements
- **Intuitive drag-and-drop mechanics** as the primary interaction method
- **Readable typography** using a simple sans-serif font family
- **Audio feedback** that complements interactions subtly

## Visual Elements

### Color Palette
- Background: Soft off-white (#F7F5F2)
- Primary gameplay elements: Bold primary colors (blue #1A73E8, red #EA4335, yellow #FBBC04)
- Secondary elements: Pastel variants of primary colors
- Text: Dark gray (#333333) for high contrast
- Highlights: Bright white (#FFFFFF) for emphasis

### Typography
- Primary font: Roboto or Open Sans
- Use weight variations instead of different fonts
- Text hierarchy through size (16pt for main interface, 12pt for secondary information)
- Minimal text - prioritize iconography where possible

### Iconography
- Simple line-based icons with consistent stroke width
- Icons should be recognizable at small sizes (24×24px)
- Animated state changes with subtle transitions
- Interactive elements should have hover/active states

## Game Interface Components

### Main Menu
- Centered title with large, simple typography
- Floating menu options with generous spacing
- Subtle parallax effect on background elements
- Animated transitions between menu screens

### Game Canvas
- Minimal UI chrome, maximum space for gameplay
- Subtle grid pattern as positioning reference
- Subtle ambient background animation for visual interest
- Important game elements pop with contrast and subtle pulsing animations

### Portal Creation and Management
- Drag-and-drop interaction for creating portals
- Portal pairs connected by color and subtle particle effects
- Portal state changes animate smoothly (opening, closing, active, inactive)
- Ghosting effects show potential placement before committing

### Game Controls
- Bottom toolbar with essential functions only
- Tools appear and disappear with smooth fade transitions
- Circular action buttons with recognizable iconography
- Tool selection highlighted with subtle glow effect

### Feedback Systems
- Success/failure animations use universally understood visual language
- Particle effects for portal activations and transfers
- Screen shake for important events (minimally used)
- Flash highlights for urgent attention items

## Interaction Design

### Core Mechanics
- **Portal Creation**: Drag from origin point to destination
- **Object Movement**: Drag objects to portal entrances
- **Portal Modification**: Tap-and-hold to access contextual menu
- **Camera Control**: Two-finger pan and pinch to zoom
- **Time Control**: Slider or button interface for game speed

### Animation Principles
- All movements follow ease-in-out curves for natural feel
- Interface elements slide into view rather than appearing abruptly
- Consistency in animation timing (quick: 0.2s, standard: 0.3s, emphasis: 0.5s)
- Animations respond to user input immediately to feel responsive

### Feedback Loop
- Visual ripples confirm touch interactions
- Subtle sound effects complement all interactions
- Success/failure states clearly communicated through animation
- Progress indicated through minimal UI elements (thin progress bars, small counters)

## Implementation Guidelines

### Performance Considerations
- Optimize for 60fps animations on all target devices
- Use hardware acceleration for animations
- Minimize DOM operations by using canvas-based rendering
- Implement efficient collision detection algorithms

### Accessibility
- Color-blind friendly design (distinguish elements by shape as well as color)
- Adjustable game speed options
- Clear visual feedback not dependent solely on audio
- Scalable UI elements

### Technical Architecture
- Separate rendering logic from game state management
- Event-driven system for UI updates
- Optimize touch handling for responsive feel
- Implement frame-skipping for performance on lower-end devices

## Level Design

### Tutorial Progression
- Progressive disclosure of mechanics
- Minimal text instructions, favor guided interaction
- Highlight new elements with subtle animations
- Success moments celebrated with satisfying visual/audio feedback

### Difficulty Curve
- Start with linear challenges, progressing to spatial puzzles
- Introduce new mechanics one at a time with breathing room
- Late-game levels combine multiple mechanics in creative ways
- Optional challenge paths for advanced players

## Sound Design

### Audio Philosophy
- Minimal, non-intrusive sounds
- Musical tones rather than realistic effects
- Audio elements that can layer harmoniously
- Volume variations based on importance of feedback

### Sound Categories
- UI interactions (clicks, swooshes)
- Portal creation/activation
- Success/failure states
- Ambient background elements
- Special events

## Mobile-Specific Considerations
- Touch targets minimum 44×44 points
- Account for finger occlusion when designing interactions
- Implement edge protection for important UI elements
- Consider portrait and landscape orientations

## Desktop-Specific Considerations
- Mouse and keyboard controls as alternatives to touch
- Hover states provide additional information
- Right-click contextual menus where appropriate
- Keyboard shortcuts for power users

## Playtesting Focus Areas
- Intuitiveness of controls without instruction
- Visibility of important elements on small screens
- Performance on target devices
- Emotional response to the interface aesthetics
- Satisfaction of interaction feedback
