# 🔍 Where to Find the Quick Test Buttons

## Step 1: Open Browser

**Open your web browser (Chrome, Firefox, Edge) and type in the address bar:**

```
http://localhost:5000
```

Press **Enter**

---

## Step 2: What You Should See

You should see a **dark blue/black themed page** with:

### 🔝 **Top of Page:**
- **Navigation Bar** (sticky at top)
  - "🛡️ AdaptivePhish" logo on left
  - "Scans Today: 0" on right

### 📊 **Middle Section:**
- **Big Title:** "Multi-Modal AI Phishing Detection"
- **3 Status Badges:**
  - 🟢 All Systems Operational
  - 🤖 3 AI Models Active
  - 🔒 100% Privacy Protected

### 📝 **Main Card (White/Gray Card):**
- **Title:** "🔍 Analyze Suspicious Content"
- **3 Tabs at top of card:**
  - 🔗 URL Analysis (should be selected/blue)
  - 📝 Text Content
  - 🖼️ Screenshot

### 🎯 **QUICK TEST BUTTONS - HERE!**

**Scroll down slightly in the main card!**

After the URL input box, you'll see:

**Label:** "⚡ Quick Tests:"

**3 Colorful Buttons in a row:**

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   ✅             │  │   ⚠️             │  │   🔴             │
│   Safe Site      │  │   Suspicious     │  │   Phishing       │
│   google.com     │  │   paypa1-...     │  │   verify-urg...  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

**These are the Quick Test buttons!**

- **Green** button (✅ Safe Site) on the left
- **Yellow** button (⚠️ Suspicious) in the middle  
- **Red** button (🔴 Phishing) on the right

---

## Step 3: Click the Green Button

Click the **"✅ Safe Site"** button (leftmost, green-themed)

---

## What Happens After Clicking:

1. **Button activates** (loading state)
2. **Wait 2-5 seconds**
3. **Results appear below:**
   - Big circular score meter (animated!)
   - Risk level bar with gradient
   - Verdict: "SAFE" in green
   - Module scores grid
   - Detection details

---

## 🚨 **If You DON'T See the Buttons:**

### Problem 1: Page Didn't Load
**Check:**
- Is the URL exactly `http://localhost:5000`?
- Do you see the dark themed page?
- Do you see "AdaptivePhish" title?

**If NO:** 
- Backend not serving frontend properly
- Try refreshing page (F5)

### Problem 2: Page Loads But No Buttons
**Check:**
- Scroll down! They might be below the fold
- Look for "⚡ Quick Tests:" label
- Look for the URL input box first

**If still not visible:**
- Press F12 → Console tab
- Look for JavaScript errors (red text)
- Take screenshot and tell me what you see

### Problem 3: Buttons Visible But Not Clickable
**Check:**
- Do they change color when you hover?
- Does cursor change to hand pointer?
- Press F12 → Console
- Click button and see if any error appears

---

## 📸 **Visual Layout:**

```
┌─────────────────────────────────────────────────────────┐
│ 🛡️ AdaptivePhish    AI Powered    Scans Today: 0   95% │ ← Navigation Bar
└─────────────────────────────────────────────────────────┘

     Multi-Modal AI Phishing Detection
     Advanced protection using Computer Vision, NLP...

   🟢 All Systems    🤖 3 AI Models    🔒 100% Privacy
      Operational        Active           Protected

┌─────────────────────────────────────────────────────────┐
│ 🔍 Analyze Suspicious Content                          │
│                                                         │
│ 🔗 URL Analysis | 📝 Text Content | 🖼️ Screenshot     │ ← Tabs
│ ─────────────                                          │
│                                                         │
│ 🌐 [Enter URL to analyze...........................]    │ ← URL Input
│                                                         │
│ [⚡ Analyze Now]                                        │ ← Analyze Button
│                                                         │
│ ─────────────────────────────────────────────────────  │
│                                                         │
│ ⚡ Quick Tests:                                         │ ← LOOK HERE!
│                                                         │
│ [✅ Safe Site]  [⚠️ Suspicious]  [🔴 Phishing]         │ ← QUICK TEST BUTTONS!
│ [google.com  ]  [paypa1-se... ]  [verify-urg...]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ **Success Looks Like:**

After clicking **"✅ Safe Site"**:

```
Results appear:

┌─────────────────────────────────────┐
│  🟢  SAFE                           │
│  This URL appears to be legitimate  │
│                                     │
│  Risk Score: 0%  [○────────────]   │
│                                     │
│  🔗 URL Analysis: 0%                │
│  🖼️ Visual Analysis: N/A            │
│  🤖 Text Analysis: N/A              │
└─────────────────────────────────────┘
```

---

## 🆘 **Still Can't Find It?**

1. **Take a screenshot** of what you see in the browser
2. **Press F12** and screenshot the Console tab
3. **Tell me:** What do you see on the page?

I'll help you debug!
