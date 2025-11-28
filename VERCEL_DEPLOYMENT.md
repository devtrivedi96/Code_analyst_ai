# 🚀 Deploy to Vercel

## Quick Deploy Steps:

### 1. **Install Vercel CLI**

```bash
npm install -g vercel
```

### 2. **Login to Vercel**

```bash
vercel login
```

### 3. **Deploy from Project Root**

```bash
cd /path/to/code_analyst
vercel
```

### 4. **Follow the prompts:**

- Confirm project settings
- Set up production deployment
- Get your live URL!

---

## Manual Setup (if needed):

### Via Vercel Dashboard:

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository
4. Framework Preset: **Other**
5. Root Directory: Leave as `.`
6. Build Command: `pip install -r requirements.txt`
7. Output Directory: `.`
8. Deploy!

---

## Environment Variables (if needed):

If you add API keys for real AI models, set them in Vercel:

- Go to Project Settings → Environment Variables
- Add `OPENAI_API_KEY`, `GOOGLE_API_KEY`, etc.

---

## Important Notes:

⚠️ **Vercel has limitations:**

- **Request Timeout**: 60 seconds for free tier
- **Memory**: 3GB limit
- **Disk**: Read-only file system (no file creation)

✅ **Your app works because:**

- Syntax checking: Fast ✓
- Code quality analysis: Fast ✓
- AI review: Simulated (no external API calls) ✓
- No database needed ✓

---

## Troubleshooting:

**Issue**: Build fails with module errors

- **Fix**: Ensure all imports in `src/app.py` match actual file structure

**Issue**: 404 on static files

- **Fix**: Vercel serves `public/` directory automatically. Move `src/static/` files there if needed.

**Issue**: Timeout errors

- **Fix**: Optimize code analysis or use environment-specific timeouts

---

## Deploy Command:

```bash
vercel --prod
```

This deploys to production URL!

---

Need help? Contact Vercel support or check the dashboard logs for errors.
