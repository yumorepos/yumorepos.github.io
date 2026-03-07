# Yumo — Developer Portfolio

A clean, minimal developer portfolio built with vanilla HTML, CSS, and JavaScript. No frameworks, no build step, no dependencies.

## Deploy

### GitHub Pages
1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set source to `main` branch, root folder
4. Your site will be live at `https://yumorepos.github.io/portfolio-website/`

### Vercel
1. Push to GitHub
2. Import the repo on [vercel.com](https://vercel.com)
3. Deploy — it auto-detects static sites

### Netlify
Drag and drop the folder at [netlify.com/drop](https://app.netlify.com/drop)

## Customize

- **Content:** Edit `index.html` directly
- **Colors/Fonts:** Modify CSS variables in `:root` at the top of `style.css`
- **Contact links:** Update the email, GitHub, and LinkedIn URLs in the Contact section

## Structure

```
├── index.html   → Content and structure
├── style.css    → All styles (dark theme, responsive)
├── main.js      → Animations, mobile menu, scroll effects
└── README.md    → This file
```

## Tech

- Zero dependencies
- Pure HTML5 + CSS3 + vanilla JS
- Google Fonts (Inter + JetBrains Mono)
- Intersection Observer for scroll animations
- Mobile-first responsive design
