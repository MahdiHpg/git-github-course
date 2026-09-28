# فصل ۲ — نصب، پیکربندی و اتصال امن به گیت‌هاب

> 🎯 **هدف:** نصب تمیز روی ویندوز، config هایی که یک بار برای همیشه می‌زنی، و اتصال به گیت‌هاب با SSH (دیگه رمز و توکن تایپ نکنی). آخر فصل یک پروژه واقعی clone می‌کنی.

---

## ۲.۱ — نصب Git روی ویندوز

1. برو به **https://git-scm.com/download/win** → آخرین نسخه (Git 2.5x) رو دانلود کن
2. موقع نصب، این گزینه‌ها مهم‌ان (بقیه پیش‌فرض):

| صفحه | گزینه | چرا |
|---|---|---|
| Select Components | پیش‌فرض (Git Bash + Git GUI تیک‌خورده) | Git Bash ترمینال ماست |
| **Choosing the default editor** | **Use Visual Studio Code as Git's default editor** ⭐ | پیام‌های کامیت و rebase با VS Code باز می‌شن — راحت‌ترین |
| Adjusting your PATH | **Git from the command line and also from 3rd-party software** (پیش‌فرض) | git در همه ترمینال‌ها در دسترس |
| HTTPS transport | OpenSSL (پیش‌فرض) | — |
| **Line ending conversions** | **Checkout Windows-style, commit Unix-style** ⭐ | پایین‌تر کامل توضیح می‌دم — مهم! |
| Terminal emulator | **Use MinTTY** (پیش‌فرض) | Git Bash بهتر از cmd |
| Experimental options | تیک نزن | — |

3. تست:

```bash
git --version
# git version 2.5x.windows.1
```

### ⚠️ داستان CRLF/LF — دردی که هر دولوپر ویندوزی یک بار می‌کشه

ویندوز خط جدید را با `CRLF` ثبت می‌کند، لینوکس/مک با `LF`. اگر تنظیم نباشه، diff های الکی پر از «کل فایل تغییر کرده» می‌شن و تیم‌های مختلط (ویندوزی+مکی) دیوانه می‌شن. راه‌حل دو لایه:

- موقع نصب: گزینه «Checkout Windows-style, commit Unix-style» = `core.autocrlf=true` — موقع checkout به CRLF تبدیل کن، موقع commit همیشه LF ذخیره کن
- بهتر از اون (روش مدرن ⭐): در **ریشه هر پروژه** فایل `.gitattributes` بذار که برای همه تیم یکسان باشه:

```bash
# .gitattributes
* text=auto eol=lf     # همه فایل‌های متنی: در مخزن LF ذخیره شو
*.png binary           # باینری‌ها دست نزن
```

---

## ۲.۲ — پیش‌گرم: دستورات پرکاربرد Git Bash

گیت یک ابزار خط فرمانه — پس خط فرمان هم باید دستت بیاد. Git Bash (که با گیت نصب شد) یک محیط لینوکسی روی ویندوزه؛ این‌ها صد درصد برای کار روزانه کافی‌ان:

```bash
pwd                     # الان کجام؟ (print working directory)
ls -la                  # لیست با جزئیات؛ -a حتی مخفی‌ها (پوشه .git!)
cd my-app               # برو به پوشه؛  cd ..  یک پله بالا؛  cd ~  خانه

mkdir docs              # پوشه بساز
touch notes.txt         # فایل خالی بساز
cp app.js app.bak.js    # کپی
mv app.js src/          # جابه‌جایی (و تغییر نام!)
rm notes.txt            # حذف فایل
rm -rf old-folder/      # حذف پوشه — ⚠️ بدون سطل بازیافت!

cat README.md           # محتوای فایل را نمایش بده
echo "hi" > file.txt    # خروجی را در فایل بریز (> بازنویسی؛ >> افزودن)
grep -rn "TODO" src/    # جست‌وجوی رشته در فایل‌ها (r=بازگشتی، n=شماره خط)
chmod +x script.sh      # قابل اجرا کردن فایل (فصل ۱۴ بهش نیاز داری)
```

مهارت‌های کوچکی که سرعتت رو چند برابر می‌کنن:

- **Tab** = تکمیل خودکار اسم فایل/پوشه — تایپ طولانی ممنوع
- **↑** = تاریخچه دستورات؛ **Ctrl+C** = قطع دستور گیرکرده؛ **clear** = پاک کردن صفحه
- `.` یعنی همین پوشه، `..` پوشه والد، `~` یعنی `C:\Users\YourUsername`
- زنجیره‌سازی: `git log --oneline | grep "feat"` — خروجی یک دستور را به دستور بعدی بده (پایپ `|`)

> 💡 همین دستورات مبنای هوک‌ها و اسکریپت‌های فصل ۱۴‌اند (`grep`، `chmod`، شل). ده دقیقه امروز، ساعتها راحتی بعداً.

---

## ۲.۳ — پیکربندی: یک بار برای همیشه

گیت سه سطح config دارد: `system` (کل ویندوز) > `global` (کاربر تو ⭐) > `local` (فقط این مخزن).

```bash
# هویت تو — با همون ایمیلی که اکانت گیت‌هابت ثبت شده! (کامیت‌ها به پروفایلت وصل می‌شن)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# شاخه پیش‌فرض جدیدها
git config --global init.defaultBranch main

# ادیتور و ابزار
git config --global core.editor "code --wait"

# پرکاربردترین alias های حرفه‌ای — یک بار بزن، عمراً پشیمون نشو
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"

# پیش‌فرض push برای شاخه‌ای که براش upstream هست
git config --global push.autoSetupRemote true

# رمز عبور/توکن رو ویندوز خودش نگه داره (برای HTTPS)
git config --global credential.helper manager
```

بعدش این رو بزن و نتیجه رو ببین:

```bash
git config --global --list
```

> 💡 `git lg` از این به بعد دستور پرتکرارت خواهد بود — گراف تاریخچه با یک جفت حرف. تو VS Code هم افزونه **GitLens** رو نصب کن؛ تاریخچه‌خوانی فوق‌حرفه‌ای داخل ادیتور.

---

## ۲.۴ — اتصال به گیت‌هاب: SSH (روش استاندارد شرکت‌ها) ⭐

دو راه احراز هویت برای push/pull داریم:

| روش | چیست | توصیه استاندارد |
|---|---|---|
| HTTPS + Personal Access Token | رمز یکبارمصرف به جای پسورد | برای کارهای موردی |
| **SSH key** | جفت‌کلید رمزنگاری؛ یک بار تنظیم، همیشه بدون رمز | ⭐ استاندارد؛ روی همه شرکت‌ها رایجه |

### ساخت کلید SSH (ویندوز، در Git Bash)

```bash
# ۱. ساخت جفت‌کلید ed25519 (استاندارد مدرن)
ssh-keygen -t ed25519 -C "you@example.com"
# Enter بزن (مسیر پیش‌فرض) و یک passphrase دلخواه (می‌تونی خالی بذاری)

# ۲. کلید عمومی رو نمایش بده و کپی کن
cat ~/.ssh/id_ed25519.pub
# ssh-ed25519 AAAAC3NzaC...xyz you@example.com
```

> 🔑 دو کلید ساخته شد: `id_ed25519` (خصوصی — **هرگز جایی نفرست/آپلود نکن!**) و `id_ed25519.pub` (عمومی — همینه که به گیت‌هاب می‌دی).

### اضافه‌کردن به گیت‌هاب

1. GitHub → پروفایل → **Settings → SSH and GPG keys → New SSH key**
2. Title: اسم کامپیوترت (مثلاً `Work-Laptop` یا `Personal-PC`)، Key: محتوای `.pub` رو paste کن
3. تست:

```bash
ssh -T git@github.com
# Hi <username>! You've successfully authenticated... 🎉
```

### و توکن (برای وقتی HTTPS خواستی)

GitHub → Settings → **Developer settings → Personal access tokens → Fine-grained tokens** → Generate: فقط دسترسی به مخزن‌های مشخص، فقط دسترسی‌های لازم (Contents: Read and write)، تاریخ انقضا مشخص. توکن مثل پسورده — فقط یک بار نمایش داده می‌شه، نگهش دار.

> 🚨 اگر روزی کلید خصوصی یا توکن لو رفت: فوراً از گیت‌هاب حذفش کن (Revoke) و یکی جدید بساز. (و اگر در کد آپلود شده بود، فصل ۱۳ سناریوی «فایل حساس در کامیت» رو ببین.)

---

## ۲.۵ — اولین مخزن: init و clone

دو راه شروع یک پروژه:

### الف) از صفر — `init`

```bash
mkdir my-app && cd my-app
git init
# Initialized empty Git repository in .../my-app/.git/
```

پوشه `.git` ساخته شد — مغز کل تاریخچه. **هیچ‌وقت داخلش دستکاری نکن** (فقط نگاه کن!).

### ب) از گیت‌هاب — `clone` (پرکاربردتر در شرکت!)

```bash
# از URL پروژه‌ای که روی گیت‌هاب داری (دکمه سبز Code → SSH):
git clone git@github.com:username/my-project.git
cd my-project
git lg    # با alias ای که زدیم — تاریخچه رو ببین!
```

جدول کارهای روز اول در هر شرکت جدید (این رو حفظ کن — دقیقاً همین کار رو می‌کنی):

```bash
# ۱. دسترسی بگیر: ایمیل شرکت رو به تیم IT بده تا به مخزن add کنن
# ۲. کلید SSH سیستمت رو به اکانت گیت‌هابت اضافه کن
# ۳. کلون کن:
git clone git@github.com:company-name/project.git
# ۴. ببین main چه خبره و برنچ محیطی بزن:
cd project && git lg
npm install   # یا هر نصبی پروژه لازم داره
```

---

## ۲.۶ — معرفی مخزن آزمایشی دوره: `git-playground`

از این فصل به بعد، همه تمرین‌ها در این زمین امن انجام می‌شه:

```bash
mkdir git-playground && cd git-playground
git init
echo "# زمین تمرین" > README.md
git add README.md
git commit -m "chore: init playground"
```

حالا یک فایل بساز و با `git status` هر لحظه ببین کجای سه‌ناحیه است — این «دیدن» عادتیه که تا آخر دوره باهاته:

```bash
echo "v1" > app.js
git st
# ?? app.js           ← Untracked: گیت هنوز نمی‌شناسدش
git add app.js
git st
# A  app.js           ← Added: در سبد کامیت بعدی
git commit -m "feat: add app v1"
git st
# nothing to commit, working tree clean ✅
```

---

## ✅ جمع‌بندی فصل

- Git Bash = ترمینال لینوکسی تو: `ls/cd/mv/rm/grep/chmod` + Tab و ↑ — پایه هوک‌های فصل ۱۴
- Git for Windows نصب کردی؛ ادیتور پیش‌فرض VS Code؛ توجه به CRLF/LF (`autocrlf` + `.gitattributes`)
- config ها یک‌بار برای همیشه: `user.name/email`، `init.defaultBranch main`، alias های `st` و `lg`
- SSH: جفت‌کلید ed25519؛ `.pub` به گیت‌هاب، کلید خصوصی محرمانه؛ `ssh -T git@github.com` تست اتصال
- `init` برای پروژه نو، `clone` برای ورود به پروژه موجود — روز اول شرکت = clone + آشنایی با `git lg`
- زمین تمرین `git-playground` آماده شد

## 📝 تمرین فصل ۲

1. هر سه alias این فصل رو بزن و `git lg` را روی یکی از مخزن‌های لوکال خود اجرا کنید.
2. کلید SSH بساز و به گیت‌هاب وصل کن (اگه از قبل داری، فقط `ssh -T` بزن و اتصال رو تأیید کن). چند کلید داری؟ `ls ~/.ssh/*.pub`
3. زمین تمرین رو بساز و چرخه کامل untracked → staged → committed رو با `git st` دنبال کن.
4. به یکی از مخزن‌های خودت `.gitattributes` با محتوای فصل اضافه کن.
5. در Git Bash: با `grep -rn "TODO" .` بگرد ببین چند TODO در پروژه‌ات مونده؛ بعد `cd ~` و `ls` — اینجا کجاست؟

<details><summary>نکته تمرین ۲</summary>

```bash
ls ~/.ssh/*.pub
ssh -T git@github.com
```
اگه خروجی `Hi <username>!` بود، همه‌چیز آماده است. چند کلید داشتن اشکالی نداره (هر دستگاه یکی)، ولی لیستش رو در گیت‌هاب گاهی مرور کن و کلید دستگاه‌های قدیمی رو حذف کن.
</details>

➡️ **فصل بعد:** هنر کامیت بامعنا — چیزی که تو تیم‌ها واقعاً بهش نمره می‌دن.
