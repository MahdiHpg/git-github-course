# فصل ۱۰ — گیت‌هاب و ریموت‌ها: push، pull، fetch و فورک

> 🎯 **هدف:** رابطه مخزن لوکالت با گیت‌هاب رو شفاف کنی: origin/upstream چین؟ فرق pull و fetch؟ فورک چیه و کی لازمه؟ آخر فصل، چرخه کامل کار با مخزن شرکتی رو بلدی.

---

## ۱۰.۱ — Remote: آدرس مخزن در دنیای بیرون

مخزن لوکالت یک **ریموت** داره: آدرسِ نسخه ابری. ببینش:

```bash
git remote -v
# origin  git@github.com:username/my-project.git (fetch)
# origin  git@github.com:username/my-project.git (push)
```

- **origin** = اسم قراردادی ریموتِ «خانه اصلی پروژه» (می‌تونه هر اسمی باشه؛ ولی origin استاندارده)
- یک مخزن می‌تونه چند ریموت داشته باشه (مثلاً origin = فورک خودت، upstream = مخزن شرکت)

شاخه‌های ریموت هم در لوکال شما آینه می‌شن:

```bash
git branch -a
# * feature/x
#   main
#   remotes/origin/main        ← آینه آخرین وضعیت ریموت (فقط با fetch تازه می‌شود)
#   remotes/origin/HEAD
```

> 🔑 **مفهوم کلیدی:** `origin/main` یک **کپی محلی از وضعیت ریموت در لحظه آخرین fetch** است — نه وضعیت زنده! تا fetch نکنی، گیت چیزی از دنیای بیرون نمی‌دونه. همه کارهای گیت لوکال، آفلاین.

## ۱۰.۲ — fetch در مقابل pull: فرقی که در شرکت مهمه

| دستور | کار | کی |
|---|---|---|
| `git fetch` | فقط *دانلود* وضعیت جدید ریموت به `origin/*` — کدت دست نمی‌خوره | می‌خوام اول ببینم چی اومده |
| `git pull` | `fetch` + `merge` (یا rebase) در شاخه فعلی | «همه‌چیز رو بیار و ادغام کن» |

```bash
git fetch origin
git lg --all                 # حالا ببین همکارت چه آورده
git diff main origin/main    # تفاوت شاخه محلی با شاخه ریموت چیست؟
git merge origin/main        # (یا rebase) — تصمیم آگاهانه!
```

> 💡 توصیه حرفه‌ای: **عادت کن fetch + نگاه + بعد ادغام.** pull کورکورانه دقیقاً همون چیزیه که merge conflict های غافلگیرکننده می‌سازه. (اگه pull می‌زنی، حرفه‌ای‌ترش: `git pull --rebase` که تاریخچه رو خطی نگه می‌داره — فصل ۸.)

## ۱۰.۳ — push و upstream

```bash
git push                     # کاری که بلدی — ولی زیر hood چی می‌کنه؟
```

اولین push یک شاخه جدید (میان‌بر مدرن — از Git 2.37+ بدون تنظیم اضافه کار می‌کنه):

```bash
git push -u origin feature/x
# -u (upstream): این شاخه لوکال را «جفت» کن با origin/feature/x
# بعد از آن، در همان شاخه فقط: git push
```

چند واقعیت push:

- push فقط کامیت‌های **جدید** رو می‌فرسته (snapshot های قبلی از قبل رفته‌ان)
- push پیش‌فرض fast-forward فقط: اگه ریموت جلوتر از تو باشه، **رد می‌شه**:
  ```
  ! [rejected] main -> main (fetch first)
  ```
  علاج درست: `git pull --rebase` بعد `push` — **هرگز** از اول force نزن!
- بازنویسی تاریخچه (rebase/amend روی شاخه شخصی push شده) → `git push --force-with-lease`

```bash
git push --delete origin feature/old     # حذف شاخه از ریموت
git push origin v1.2.0                   # پوش تگ‌ها (فصل ۹)
```

## ۱۰.۴ — clone، fork و روابطشون

سه راه ورود به یک مخزن گیت‌هاب:

| روش | کی | در شرکت |
|---|---|---|
| **clone** مستقیم مخزن | عضو تیم/organization هستی با دسترسی write ⭐ | ۹۵٪ موارد |
| **fork + clone** | پروژه open source ای که maintainer اش نیستی | contribution به پروژه‌های خارجی |
| دانلود ZIP | فقط نگاه | (گیت نداره! رشدت رو نشون نده 😄) |

### فرق fork با clone

- **clone** = کپی لوکال از مخزن (توی سیستمت)
- **fork** = کپی کامل مخزن **در اکانت گیت‌هاب خودت** (روی ابر)

الگوی استاندارد contribution به open source:

```bash
# ۱. روی گیت‌هاب: Fork بزن → github.com/your-username/cool-lib ساخته می‌شود
git clone git@github.com:your-username/cool-lib.git
cd cool-lib

# ۲. ریموت مخزن اصلی را اضافه کن (برای همگام موندن):
git remote add upstream git@github.com:original/cool-lib.git
git remote -v
# origin    git@github.com:your-username/cool-lib.git   (مخزن فورک‌شده شخصی — مقصد push)
# upstream  git@github.com:original/cool-lib.git    (اصلی — فقط fetch)

# ۳. همیشه قبل از شروع کار، از منبع اصلی تازه کن:
git fetch upstream
git switch main && git merge upstream/main   # یا rebase
git push origin main

# ۴. شاخه بزن، کار کن، push به origin (فورک خودت)،
#    و از گیت‌هاب به مخزن اصلی Pull Request بزن (فصل ۱۱)
```

## ۱۰.۵ — ساخت مخزن و حرفه‌ای‌سازی پروژه‌ها

روی گیت‌هاب: **New repository** → اسم، عمومی/خصوصی، تیک **Add a README**. بعد از لوکال:

```bash
git remote add origin git@github.com:your-username/new-project.git
git push -u origin main
```

چند تکلیف یک‌بار-مصرف که پروژه‌هات رو از «تمرینی» به «حرفه‌ای» تبدیل می‌کنه:

| فایل | چرا |
|---|---|
| `README.md` خوب | اولین چیزی که مصاحبه‌گر می‌بینه: چی، چرا، چطور اجرا شه |
| `.gitignore` از روز اول | node_modules و .env نریز بالا (فصل ۹) |
| توضیحات (About) + topics | قابلیت جستجو در گیت‌هاب |
| لایسنس (MIT و...) | پروژه‌ی open source بدون لایسنس = «همه حق محفوظ» به صورت پیش‌فرض |

## ۱۰.۶ — گردش کامل یک روز کاری در شرکت

```bash
git switch main && git pull            # صبح: تازه‌سازی
git switch -c fix/invoice-total        # شاخه کار
# ... کد، تست ...
git add -p && git commit -m "fix(invoice): round totals correctly"
git fetch origin                        # ببین main تکون خورده؟
git rebase origin/main                  # (اختیاری) تاریخچه خطی
git push -u origin fix/invoice-total    # اولین پوش شاخه
# → روی گیت‌هاب: Compare & pull request (فصل ۱۱!)
```

---

## ✅ جمع‌بندی فصل

- `origin` = آدرس مخزن ابری؛ `origin/main` = آینه لوکالِ ریموت (فقط با fetch تازه می‌شه)
- **fetch = فقط دانلود؛ pull = fetch + ادغام.** عادت حرفه‌ای: fetch → نگاه → ادغام (`--rebase`)
- `push -u` جفت‌سازی شاخه لوکال با ریموت؛ رد شدن push یعنی «اول pull --rebase کن» — نه force!
- **fork = کپی مخزن در اکانتت** برای contribution به پروژه‌های خارجی؛ داخل شرکت معمولاً clone مستقیم + شاخه
- day-1 شرکت: کلید SSH → clone → fetch → شاخه جدید

## 📝 تمرین فصل ۱۰

1. در یکی از پروژه‌های خود دستور `git remote -v` را اجرا کنید — SSH هست یا HTTPS؟ (اگه HTTPS با رمز کار می‌کنی، مهاجرتش کن به SSH — با `git remote set-url`)
2. روی گیت‌هاب یک مخزن جدید خالی بساز و از لوکال بهش push کن — چرخه کامل remote add → push -u.
3. یک پروژه محبوب open source رو fork کن، clone اش کن، upstream رو add کن و `git fetch upstream` بزن. (بدون تغییری — فقط زیرساخت contribution رو آماده کنی.)
4. `git fetch` بزن و بعد `git diff main origin/main` — فرق لوکالت با ریموت چیه؟

<details><summary>راهنمای تمرین ۱</summary>

```bash
git remote -v
git remote set-url origin git@github.com:USER/REPO.git   # مهاجرت به SSH
ssh -T git@github.com                                     # تست
git fetch && git push                                     # تأیید نهایی
```
</details>

➡️ **فصل بعد:** Pull Request — جایی که همکاری واقعی گیت‌هابی شکل می‌گیره.
