# فصل ۹ — Stash، Tag و gitignore: ابزارهای کیفیت زندگی

> 🎯 **هدف:** سه ابزاری که هر روزِ کار تو رو راحت‌تر می‌کنن: نگه‌داشتن کار نیمه‌تمام (stash)، نشونه‌گذاری نسخه‌ها (tag)، و بی‌خیال شدنِ فایل‌های محلی (gitignore).

---

## ۹.۱ — Stash: کمد موقت تغییرات 🧥

سناریوهای واقعی:
- داری روی feature کار می‌کنی؛ باگ urgent گزارش می‌شه — کدهای نیمه‌تمامت رو **نه کامیت** می‌خوام نه حذف
- می‌خوای `git pull` بزنی ولی ویرایش‌های محلی جلوی merge رو می‌گیرن
- می‌خوای فقط یه فایل رو ببینی چطوری «قبل از تغییرات» بود

```bash
git stash                # تغییرات (staged + unstaged) برو توی کمد
git stash -u             # فایل‌های untracked هم بیا (خیلی وقت‌ها لازمه!)

# ... حالا working directory تازه مثل آخرین کامیت — هر کاری بخوای بکن ...

git stash pop            # برگردون آخرین stash و از لیست حذفش کن
git stash apply          # برگردون ولی در لیست بمونه
git stash list           # کمدها: stash@{0}, stash@{1}, ...
git stash pop stash@{2}  # یک کمد خاص
git stash drop stash@{0} # دور انداختن یک stash
```

> ⚠️ stash یک کامیت واقعیه که «قلم‌زده» شده — پس گم‌شدنش هم با reflog برطرف می‌شه. ولی سبک ذهنی درست: stash = کوتاه‌مدت (چند ساعت/یک روز)؛ کار طولانی = شاخه.

الگوی پرکاربرد در شرکت:

```bash
git stash -u
git switch main && git pull
git switch -c hotfix/critical
# ... فیکس، کامیت، push، PR ...
git switch feature/my-work
git stash pop
```

## ۹.۲ — Tag: نشان نسخه‌ها 🏷️

کامیت‌ها زنجیره‌ان؛ tag یعنی «این کامیت، نسخه رسمی v1.2.0 هست». دو نوع:

```bash
git tag                          # لیست تگ‌ها
git tag v1.0.0                   # سبک: فقط اشاره‌گر
git tag -a v1.0.0 -m "اولین ریلیز پایدار"    # ⭐ سنگین (annotated): پیام+نام+تاریخ

git show v1.0.0                  # جزئیات تگ
git push origin v1.0.0           # ⚠️ تگ‌ها با push معمولی نمی‌روند!
git push origin --tags           # یا همه را بفرست
git switch v1.0.0                # سفر به وضعیت آن نسخه (detached — فصل ۱۳)
```

### Semantic Versioning (قواعد شماره نسخه)

`v<MAJOR>.<MINOR>.<PATCH>` — مثلاً `v2.3.1`:

| جزء | بالا می‌ره وقتی | مثال |
|---|---|---|
| MAJOR | تغییر **شکست‌دهنده** (API قبلی می‌شکنه) | 2.0.0 |
| MINOR | فیچر جدید سازگار | 2.1.0 |
| PATCH | فیکس باگ | 2.1.1 |

در گیت‌هاب، از یک تگ یک **Release** می‌سازی (صفحه Releases → Draft a new release) با release notes — جایی که نسخه‌های محصولت رسمی می‌شن.

## ۹.۳ — gitignore: فایل‌هایی که گیت نبینه 🙈

```bash
# .gitignore (در ریشه مخزن)
node_modules/          # نصب‌شونده‌ها — هیچ‌وقت
.env                   # ⭐ رمزها و کلیدها — هیچ‌وقت!
dist/  .next/          # خروجی build
*.log  .DS_Store
coverage/
.vscode/               # تنظیمات شخصی ادیتور (یا با جزئیات: .vscode/settings.json)
```

الگوها:

| الگو | معنی |
|---|---|
| `*.log` | همه log ها در همه زیرپوشه‌ها |
| `/dist` | فقط dist در ریشه |
| `build/` | هر پوشه build در هر عمقی |
| `!important.log` | استثنا — این را ignore نکن |
| `debug?.js` | ? = یک کاراکتر دلخواه |
| `**/temp/*` | هر پوشه temp در هر عمقی |

> 🚨 **قانون امنیتی #1 گیت:** `.env` و کلید API و پسورد هرگز به مخزن نمی‌رن — حتی مخزن خصوصی! (فصل ۱۳: اگر رفت، چیکار کنی.) پیشنهاد: نمونه امن بذار: `.env.example` با مقادیر ساختگی commit می‌شه و بقیه کپی می‌کنن.

### الگوی مفید: فایل‌هایی که *سراسری* می‌خوای ignore بشن (برای خودت، نه تیم)

```bash
git config --global core.excludesfile ~/.gitignore_global
# در آن فایل: .DS_Store، Thumbs.db و ...
```

### نکته‌ای که همه یک بار گیرش می‌افتن: ignore کردن فایلی که قبلاً commit شده!

gitignore فقط فایل‌های **untracked** رو نادیده می‌گیره. فایل tracked رو باید اول از ایندکس دربیاری:

```bash
git rm --cached .env          # از مخزن حذف، از دیسک نمی‌پره
echo ".env" >> .gitignore
git commit -m "chore: remove .env from tracking"
```

## ۹.۴ — gitattributes (یادآوری) و `bisect` (پاداش ویژه 🕵️)

- `.gitattributes` فصل ۲ دیدی — قوانین فایل‌ها (eol، binary).
- پاداش: باگ رو نمی‌دونی کدوم کامیت معرفی کرده؟ جستجوی دودویی خودکار:

```bash
git bisect start
git bisect bad               # الان باگ داره
git bisect good v1.0.0       # این نسخه سالم بود
# گیت وسط می‌رود؛ تست می‌کنی و می‌گویی:
git bisect good              # یا bad — تا کامیت مقصر پیدا شود
git bisect reset
```

با ۱۰۰۰ کامیت، فقط ~۱۰ تست لازمه. ابزار «کارمنده که شب‌ها برات کار می‌کنه».

---

## ✅ جمع‌بندی فصل

- `stash -u` کار نیمه‌تمام رو موقتاً کنار می‌ذاره؛ pop برمی‌گردونه؛ برای کارهای بلند شاخه بزن نه stash
- تگ annotated برای نسخه‌ها؛ **تگ‌ها جدا push می‌شن**؛ semver: MAJOR.MINOR.PATCH
- `.gitignore` همیشه از روز اول: `node_modules/`، `.env`، خروجی build؛ فایل tracked باید با `rm --cached` آزاد شه
- `bisect` = جستجوی دودویی باگ در تاریخچه

## 📝 تمرین فصل ۹

1. زمین تمرین: تغییراتی در دو فایل بده + یک فایل جدید بساز؛ `stash` بزن (بدون -u) و بعد `pop` — فایل جدید برگشت؟ چرا؟ بعد با `-u` تکرار کن.
2. برای زمین تمرین سه تگ بزن (`v0.1.0` و ...) و سفر کن: `git switch v0.1.0` — پیام HEAD چی می‌گه؟ (`git switch main` برای برگشت!)
3. یک `.gitignore` کامل برای پروژه Next.js بنویس (بدون نگاه به جواب).
4. (چالش) با bisect: در زمین تمرین ۱۰ کامیت بزن که در کامیت ۷ یک باگ «معرفی» شده؛ بعد با bisect پیداش کن.

<details><summary>جواب تمرین ۳</summary>

```bash
# .gitignore برای Next.js
node_modules/
.next/
out/
build/
.env*.local
.env
.vercel
*.tsbuildinfo
next-env.d.ts      # (نسل جدید خودکار تولید می‌شود — بحث‌برانگیز، معمولاً ignore می‌شود)
.DS_Store
npm-debug.log*
```
جواب تمرین ۱: نه — بدون `-u`، فایل untracked در stash نمی‌آید و سرجاش می‌ماند.
</details>

➡️ **فصل بعد:** بالاخره وارد گیت‌هاب عمیق می‌شویم — ریموت‌ها، push/pull/fetch و تفاوت‌های ظریفشون.
