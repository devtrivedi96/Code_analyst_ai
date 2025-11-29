# 🤖 AI Integration Setup Guide

This project now includes real AI integration with Google Gemini, OpenAI GPT-4, and Anthropic Claude. Follow this guide to set up your preferred AI model.

---

## **Option 1: Google Gemini (Recommended - Free Tier Available)**

### **Step 1: Get API Key**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click **"Create API Key"**
3. Copy the API key

### **Step 2: Set Environment Variable**

**For Linux/Mac (Bash/Zsh):**

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**For Windows (PowerShell):**

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Permanently (Linux/Mac) - Add to ~/.bashrc or ~/.zshrc:**

```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### **Step 3: Run the Application**

```bash
cd /home/dev-trivedi/Public/Projects/AI/code_analyst
source venv/bin/activate
python3 src/app.py
```

### **Step 4: Test**

- Open browser to `http://localhost:5000`
- Paste some code
- Select **"Gemini Pro"** from AI Model dropdown
- Click **"Analyze Code"**
- Watch the magic happen! ✨

---

## **Option 2: OpenAI GPT-4**

### **Step 1: Get API Key**

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the API key

### **Step 2: Set Environment Variable**

**For Linux/Mac:**

```bash
export OPENAI_API_KEY="sk-..."
```

**For Windows:**

```powershell
$env:OPENAI_API_KEY="sk-..."
```

### **Step 3: Run**

```bash
source venv/bin/activate
python3 src/app.py
```

### **Step 4: Test**

- Select **"GPT-4"** from AI Model dropdown
- Note: OpenAI charges per token (around $0.03 per analysis)

---

## **Option 3: Anthropic Claude**

### **Step 1: Get API Key**

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create API key
4. Copy it

### **Step 2: Set Environment Variable**

**For Linux/Mac:**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**For Windows:**

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### **Step 3: Run**

```bash
source venv/bin/activate
python3 src/app.py
```

### **Step 4: Test**

- Select **"Claude"** from AI Model dropdown

---

## **🔧 How It Works**

### **Flow Diagram:**

```
User Code
    ↓
[Paste Code] → [Select AI Model] → [Click Analyze]
    ↓
Backend (app.py)
    ↓
[Check for API Key in Environment]
    ↓
If GEMINI_API_KEY set → Use Gemini
If OPENAI_API_KEY set → Use OpenAI
If ANTHROPIC_API_KEY set → Use Claude
Otherwise → Use Fallback Review
    ↓
Send code to AI API with prompt
    ↓
Parse AI response
    ↓
Return structured result
    ↓
Frontend displays formatted review
```

### **AI Review Includes:**

✅ Summary of what code does  
✅ 3-5 specific improvement suggestions  
✅ Potential bugs or issues  
✅ Code quality rating (1-10)  
✅ Overall recommendation

---

## **💰 Cost Comparison**

| Model      | Cost                | Speed       | Quality            |
| ---------- | ------------------- | ----------- | ------------------ |
| **Gemini** | Free (limited)      | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Good      |
| **GPT-4**  | $0.03-0.06/analysis | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Best    |
| **Claude** | $0.01-0.02/analysis | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent |

**Recommended:** Start with **Gemini** (free), upgrade to **GPT-4** for production.

---

## **🚀 Quick Start (Gemini)**

### **1-Minute Setup:**

```bash
# 1. Get free API key from https://aistudio.google.com/app/apikeys

# 2. Set it
export GEMINI_API_KEY="your-key"

# 3. Run app
cd /home/dev-trivedi/Public/Projects/AI/code_analyst
source venv/bin/activate
python3 src/app.py

# 4. Open http://localhost:5000 in browser

# 5. Paste code and analyze!
```

---

## **✅ Verify Setup**

### **Check if API key is detected:**

```bash
python3 -c "import os; print('GEMINI_API_KEY set!' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

### **Test the integration:**

```bash
python3 << 'EOF'
import os
import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello! Can you help me?")
    print("✅ Gemini API working!")
    print(response.text[:100])
else:
    print("❌ API key not set")
EOF
```

---

## **🐛 Troubleshooting**

### **Issue: "GEMINI_API_KEY environment variable not set"**

**Solution:** Make sure you exported the API key:

```bash
export GEMINI_API_KEY="your-key"
```

### **Issue: "Invalid API key"**

**Solution:**

- Check you copied the key correctly
- Generate a new key if needed
- Ensure no extra spaces

### **Issue: "API quota exceeded"**

**Solution:**

- For Gemini: Wait 60 seconds (rate limit)
- For OpenAI: Check your credits/billing
- Use fallback for now

### **Issue: AI review shows "API not configured"**

**Solution:**

- Your selected model's API key isn't set
- Try another model
- Or set up the API key for your preferred model

---

## **📝 Environment File (.env)**

For easier management, create a `.env` file:

```bash
# Create file
cat > /home/dev-trivedi/Public/Projects/AI/code_analyst/.env << 'EOF'
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
EOF
```

Then load it before running:

```bash
source .env
source venv/bin/activate
python3 src/app.py
```

---

## **🔐 Security Best Practices**

⚠️ **NEVER commit API keys to git!**

1. Add `.env` to `.gitignore`:

```bash
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

2. Use environment variables only
3. Rotate keys regularly
4. Use separate keys for dev/production
5. Monitor usage on provider dashboard

---

## **📊 Monitoring API Usage**

### **Gemini:** https://aistudio.google.com/app/apikeys

### **OpenAI:** https://platform.openai.com/account/usage/overview

### **Claude:** https://console.anthropic.com/usage

---

## **🎯 Next Steps**

1. ✅ Choose your AI model (Gemini recommended)
2. ✅ Get API key from provider
3. ✅ Set environment variable
4. ✅ Run the app
5. ✅ Test with sample code
6. ✅ Deploy to Vercel (if needed)

---

## **📞 Support**

If you encounter issues:

1. Check logs: `tail -f ~/.local/share/ai-code-analyst/logs`
2. Verify API key: `echo $GEMINI_API_KEY`
3. Test API connection: See "Verify Setup" section above
4. Check provider dashboard for errors

---

**Happy analyzing! 🚀**
