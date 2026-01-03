# Testing Guide

## Quick Start

1. **Install Dependencies** (if not already installed):
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Open in Browser**:
   - The server will start on `http://localhost:5173` (or another port if 5173 is busy)
   - Open the URL shown in your terminal in your browser

## What to Test

### Visual Testing
- ✅ **Landing Page**: Check that all sections render correctly
- ✅ **Hero Section**: Verify the hero image and text display properly
- ✅ **Features Section**: Check that statistics and icons are visible
- ✅ **Testimonials**: Verify customer testimonials are displayed
- ✅ **FAQ Section**: Test accordion functionality (click to expand/collapse)
- ✅ **Navigation**: Check top navigation menu
- ✅ **Footer**: Verify footer links and social media icons

### Functional Testing
- ✅ **Responsive Design**: Resize browser window to test mobile/tablet views
- ✅ **Images**: Verify all images load correctly (no broken images)
- ✅ **Buttons**: Test all CTA buttons (Book a Demo, Start Free Trial, etc.)
- ✅ **Scroll Behavior**: Test smooth scrolling through the page
- ✅ **Interactive Elements**: Test hover effects on cards and buttons

### Browser Compatibility
Test in multiple browsers:
- Chrome/Edge
- Firefox
- Safari

## Build for Production

To create a production build:
```bash
npm run build
```

The built files will be in the `dist/` directory.

## Troubleshooting

### Port Already in Use
If port 5173 is busy, Vite will automatically use the next available port. Check the terminal output for the actual URL.

### Images Not Loading
- Verify all image files exist in `src/assets/`
- Check browser console for 404 errors
- Ensure image paths are correct (should be `../assets/filename.png`)

### Styling Issues
- Clear browser cache
- Check that Tailwind CSS is properly configured
- Verify `src/styles/index.css` is imported in `main.tsx`

