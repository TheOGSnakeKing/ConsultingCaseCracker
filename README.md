# Case Cracker 🧮

Mental math flashcard app for consulting interview prep.

## Features

- **200+ questions** across fractions, percentages, multiplication, profit/margin, time conversions, market sizing, and case scenarios
- **Spaced repetition** - wrong answers repeat 3 times at increasing intervals
- **User profiles** - login/register with username and password
- **Session history** - track your progress with detailed question-by-question logs
- **Friends feed** - see everyone's stats and compete!
- **Mobile-friendly** - swipe gestures and responsive design

## Deploy to Render (Free)

### Step 1: Push to GitHub

1. Create a new GitHub repository
2. Push these files:
```bash
cd C:\Users\PC\Desktop\Ammu\files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/case-cracker.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New > Web Service**
3. Connect your GitHub account
4. Select your `case-cracker` repository
5. Render will auto-detect the settings from `render.yaml`
6. Click **Create Web Service**
7. Wait 2-3 minutes for deployment
8. Your app will be live at `https://case-cracker.onrender.com` (or similar)

### Step 3: Share!

Share the URL with anyone - they can access it from anywhere in the world!

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:9000
```

## Files

- `app.py` - Flask server (production)
- `server.py` - Simple Python server (local dev)
- `consulting-math-quiz.html` - The main app
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment config

## Note on Data Persistence

The free Render tier has ephemeral storage - data may reset when the server sleeps (after 15 min of inactivity). For permanent data storage, you can upgrade to add a database, or the app will simply start fresh.

For your wife's interview prep, this should be fine - the learning happens in the practice, not in saving historical stats forever! 😄
