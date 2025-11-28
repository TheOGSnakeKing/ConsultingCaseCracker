# Case Cracker 🧮💼

**A labor of love for my wife's consulting interview prep!**

My wife was preparing for MBA consulting interviews and needed to practice mental math. Instead of using boring flashcard apps, I thought "Why not build something custom?" ...and then I may have gone a *little* overboard. 😅

What started as a simple flashcard app turned into a full-fledged learning platform with user accounts, spaced repetition, friend leaderboards, and cloud deployment. Classic engineer move, right?

Feel free to use it for your own consulting prep, or just to flex your mental math skills!

---

## ✨ Features

- **200+ questions** across fractions, percentages, multiplication, profit/margin, time conversions, market sizing, and case scenarios
- **Spaced repetition** - wrong answers repeat 3 times at increasing intervals (the science-backed way to actually learn!)
- **User profiles** - login/register to track your progress
- **Session history** - detailed question-by-question logs with timestamps in Central Time
- **Friends feed** - see everyone's stats and have some friendly competition
- **Mobile-friendly** - swipe left (wrong) or right (correct), works great on phones
- **Keyboard shortcuts** - Space to flip, Arrow keys to answer, H for hints

---

## 🚀 Quick Start - Use It Now!

**The app is already deployed and ready to use:**

### 👉 [https://consultingcasecracker.onrender.com](https://consultingcasecracker.onrender.com)

Just create an account and start practicing! Your progress is saved to the cloud.

> ⏳ **First load may take 30-50 seconds!** The free Render tier puts the app to sleep after 15 minutes of inactivity. When you first visit, you might see a loading screen while the server wakes up. Grab a coffee, it'll be ready in a moment. After that first load, everything is snappy!

---

## 💻 Run Locally

Want to run it on your own machine? Here's how:

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Navigate to the project folder
cd C:\Users\PC\Desktop\Ammu\files

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open your browser to:
# http://localhost:9000
```

That's it! The app will connect to the cloud database, so your data syncs whether you use it locally or on the web.

---

## 🛠️ Deploy Your Own Instance

Want to deploy your own version? Here's the setup:

### GitHub Repository

The code is on GitHub: [https://github.com/TheOGSnakeKing/ConsultingCaseCracker](https://github.com/TheOGSnakeKing/ConsultingCaseCracker)

### Render Deployment

1. Fork the repo to your GitHub
2. Go to [render.com](https://render.com) and sign up (free)
3. Click **New > Web Service**
4. Connect your GitHub and select the forked repo
5. Render auto-detects settings from `render.yaml`
6. Click **Create Web Service**
7. Wait 2-3 minutes - done!

---

## 🗄️ Database Info

The app uses **MongoDB Atlas** (free tier) for persistent data storage. User accounts, session history, and stats are all stored in the cloud.

### A Note About Security 🔐

*Yes, I know* - the MongoDB connection string with the password is hardcoded in `app.py`. This is a fun personal project, not a bank. For a production app, you'd want to:
- Use environment variables for secrets
- Set up proper authentication
- Not commit passwords to GitHub

But for a flashcard app shared among friends and family? It works fine. If you're forking this for your own use, maybe change that password. 😉

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `app.py` | Flask server with API routes |
| `consulting-math-quiz.html` | The entire frontend (HTML/CSS/JS) |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |
| `server.py` | Simple Python server (legacy, for basic local dev) |

---

## 🎯 Question Categories

- **Fractions** - Convert fractions to percentages (1/7 = 14.29%? You'll know it cold!)
- **Percentages** - Calculate percentages of numbers quickly
- **Multiplication** - Mental math tricks (25 × 36 = 900, because 36÷4×100!)
- **Profit & Margin** - The consulting classics
- **Time Conversions** - Hours in a year? Working hours? Got it.
- **Market Sizing** - Population-based calculations
- **Case Scenarios** - Full case-style word problems

---

## 💡 Tips for Consulting Interviews

1. **Practice daily** - 15-20 minutes is enough
2. **Focus on patterns** - Most mental math is pattern recognition
3. **Use the hints** - They teach you the shortcuts
4. **Don't memorize, understand** - Know WHY 1/7 ≈ 14.29%
5. **Speed comes with accuracy** - Get it right first, then get fast

---

## ❤️ Acknowledgments

Built with love, caffeine, and the motivation of wanting my wife to crush her interviews.

She did. 🎉

---

*If you find this helpful, maybe buy me a coffee sometime. Or just ace your interview and tell me about it!*
