# 🚀 Quick Start - Real AI Integration Demo

## **1-Minute Setup (Google Gemini - Free)**

### **Step 1: Get Free API Key**

```
1. Go to: https://aistudio.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key
```

### **Step 2: Set the API Key**

```bash
# In the terminal where Flask is running, CTRL+C to stop
# Then run:

export GEMINI_API_KEY="AIzaSy..."  # Replace with your key
python3 src/app.py
```

### **Step 3: Open Browser**

```
http://localhost:5000
```

### **Step 4: Test It**

```python
# Paste this code into the textarea:
def add_numbers(a, b):
    return a + b

result = add_numbers(10, 5)
print(result)
```

- Select **"Gemini Pro"** from dropdown
- Click **"Analyze Code"**
- Watch the magic! ✨

---

## **What You'll See**

The AI will provide:

✅ **Summary:** "This code defines a simple function that adds two numbers and prints the result..."

✅ **Suggestions:**

- Add type hints: `def add_numbers(a: int, b: int) -> int:`
- Add docstring explaining parameters
- Consider error handling for invalid inputs
- Use more descriptive names if applicable

✅ **Issues:** No critical issues found

✅ **Quality Rating:** 8/10

✅ **Recommendation:** Good simple function! Add type hints and docstrings for production code.

---

## **Real AI Models Available**

| Model      | Setup | Cost      | Speed       |
| ---------- | ----- | --------- | ----------- |
| **Gemini** | 5 min | FREE      | ⚡ Fast     |
| **GPT-4**  | 5 min | $0.03/req | ⚡⚡ Medium |
| **Claude** | 5 min | $0.01/req | ⚡⚡ Medium |

---

## **Try It Now!**

### **Option A: With API Key (Full Features)**

```bash
export GEMINI_API_KEY="your-key-here"
python3 src/app.py
```

Then select "Gemini Pro" in the UI and analyze!

### **Option B: Without API Key (Fallback Mode)**

```bash
python3 src/app.py
```

Still works! Will show helpful fallback suggestions.

---

## **Live Testing**

Currently running at: **http://localhost:5000**

Try analyzing this code:

```python
age = "20"
print(age + 5)
```

You should see:

- ✅ Syntax Check: Valid
- ✅ Code Quality: 2 lines
- 🔍 Logic Analysis: **Type Mismatch error detected**
- ✨ Code Practices: Info
- 🤖 AI Review: **Real AI suggestions** (if API key set)

---

## **Architecture**

```
Your Code
    ↓
Browser → Flask Backend
    ↓
5 Analyzers (Syntax, Quality, Logic, Practices)
    ↓
AI Module:
├─ Checks for GEMINI_API_KEY
├─ If found → Calls Gemini API
├─ If not found → Returns helpful fallback
    ↓
Response with AI insights
    ↓
Browser displays results
```

---

## **Files Changed**

✅ `src/analyzer/ai_reviewer.py` - Real AI integration  
✅ `src/static/script.js` - Better UI for AI results  
✅ `src/app.py` - Proper response formatting  
✅ `AI_SETUP_GUIDE.md` - Complete setup guide  
✅ `REAL_AI_INTEGRATION.md` - Technical documentation

---

## **Next Actions**

1. ✅ **Get API Key** from https://aistudio.google.com/app/apikeys
2. ✅ **Set it:** `export GEMINI_API_KEY="..."`
3. ✅ **Restart app** (stop and re-run)
4. ✅ **Test in browser** at http://localhost:5000
5. ✅ **See real AI results!** 🎉

---

## **Troubleshooting**

**Q: App shows "not set"?**

```bash
# Check if key is set
echo $GEMINI_API_KEY  # Should show your key

# If empty, set it again
export GEMINI_API_KEY="AIzaSy..."
```

**Q: Still showing fallback?**

- Make sure you restarted Flask after setting the key
- Verify the key is correct (no spaces)
- Check https://aistudio.google.com/app/apikeys that key still exists

**Q: Got a different error?**

- Check Flask logs for the error
- Verify internet connection
- Try with GPT-4 instead (different provider)

---

## **Support**

- Full setup guide: `AI_SETUP_GUIDE.md`
- Technical docs: `REAL_AI_INTEGRATION.md`
- Web UI: http://localhost:5000

---

**Ready to see real AI in action? 🚀**

Get your free Gemini API key and start analyzing! ✨
