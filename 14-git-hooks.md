# فصل ۱۴ — Git Hooks: نگهبان‌های خودکار روی خط تولید 🛡️

> 🎯 **هدف:** اسکریپت‌هایی که گیت خودش در لحظه‌های مشخص اجرا می‌کند — قبل از کامیت، روی پیام، قبل از push. نتیجه: خطاهای تکراری (پیام بی‌قاعده، `.env` توی کامیت، push با تست قرمز) از «یادم نمی‌آد» تبدیل می‌شه به «غیرممکنه».

---

## ۱۴.۱ — Hook چیست؟

Hook یعنی «قلاب»: گیت در نقاط مشخص چرخه‌اش می‌پرسه «اسکریپتی داری اجرا کنم؟». دو خانواده:

| خانواده | کجا اجرا می‌شه | مثال | سرنوشت در دنیای واقعی |
|---|---|---|---|
| **Client-side** | روی سیستم تو | `pre-commit`، `commit-msg`، `pre-push`، `post-merge` | درسیِ همین فصل — با Husky به تیم می‌رسه |
| **Server-side** | روی سرورِ مخزن (قبل از قبول push) | `pre-receive`، `update` | روی گیت‌هاب بهش دسترسی نداری — معادلش **Rulesets و CI** است (فصل ۱۱ و ۱۵) |

> 🎯 قاعده طلایی هوک‌ها: **exit code همه‌چیز است.** اسکریپت با `0` تمام شود = «اجازه بده»؛ با غیر صفر = «عملیات لغو». به همین سادگی یک نگهبان می‌سازی.

هوک‌های کلید که در این فصل می‌سازیم:

- `pre-commit` — قبل از ساخت کامیت (محتوا را ببین، اجازه/رد)
- `commit-msg` — پیام کامیت را ببین (محتوای کامیت را نه!)
- `pre-push` — آخرین سد قبل از رفتن به سرور
- `post-merge` — بعد از pull/merge موفق (مثلاً `npm install` خودکار)

## ۱۴.۲ — تور پوشه hooks و فعال‌سازی

یادته در تور `.git` (فصل ۴) پوشه‌ای دیدی که ورش نداشتیم؟ حالا نوبتشه:

```bash
ls .git/hooks/
# applypatch-msg.sample   pre-commit.sample   commit-msg.sample ...
# pre-push.sample         post-merge.sample   ...
```

- هر `.sample` یک نمونه‌ی آماده و *غیرفعال* است — سند رسمی: فقط کپی‌ش کن بدون پسوند
- اسم فایل دقیقاً باید نام هوک باشد (`pre-commit`)، بدون پسوند
- در Git Bash باید executable بشه: `chmod +x .git/hooks/pre-commit`
- زبانش فرقی نمی‌کند: شل، پایتون، نود... هر برنامه‌ی قابل اجرا با shebang درست

```bash
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit     # فعال شد — همین!
```

> 🚨 **نکته تیمی مهم:** چون هوک‌ها داخل `.git` اند، **نسخه‌بندی نمی‌شن** — با push به همکارت نمی‌رسن! راه‌حل: بخش ۱۴.۶ (`core.hooksPath` و Husky).

## ۱۴.۳ — اولین نگهبان: pre-commit

سناریوی واقعی: هیچ‌وقت نباید `.env` (یا هر فایل حساس/زباله‌ی مشخص) کامیت بشه — حتی اگر یک بار وسط شب حواست پرت شد:

```sh
#!/bin/sh
# .git/hooks/pre-commit — اجازه نمی‌دهد .env کامیت شود
if git diff --cached --name-only | grep -q "^\.env$"; then
  echo "🚫 .env نمی‌تواند کامیت شود!"
  echo "   اصلاح:  git restore --staged .env"
  exit 1
fi
exit 0
```

ابزاری که اینجا نجاتت می‌دهد:

```bash
git diff --cached --name-only   # فهرست دقیق فایل‌های staged در این کامیت
```

تستش کن: `.env` را بساز، `git add` کن و کامیت بزن — گیت عملیات را رد می‌کند و پیام تو را می‌بینی. کامیت رخ *نمی‌دهد*، کدهای staged هم دست‌نخورده می‌مانند (فقط اجازه داده نشد).

> 💡 ایده‌های pre-commit واقعی: بازداشتن `console.log` در شاخه‌های release، جلوگیری از کامیت فایل‌های `*.local`، اجرای `eslint` روی فایل‌های staged. (فایل حساسِ رفته در تاریخچه؟ دیر شد — فصل ۱۳ سناریوی ۹.)

## ۱۴.۴ — commit-msg: پلیس Conventional Commits (پیوند فصل ۳)

فصل ۳ استاندارد پیام‌ها (`feat:`، `fix:` و...) رو یاد گرفتی. حالا تضمینش کن:

```sh
#!/bin/sh
# .git/hooks/commit-msg — پیام باید Conventional باشد
msg="$(cat "$1")"
pattern="^(feat|fix|chore|docs|style|refactor|perf|test|build|ci)(\(.+\))?!?: .+"
if ! echo "$msg" | grep -qE "$pattern"; then
  echo "🚫 پیام کامیت معتبر نیست. مثل:  feat: add login form"
  echo "   کامیت لغو شد — پیام را اصلاح و دوباره کامیت بزن."
  exit 1
fi
```

دو نکته ظریف:
- آرگومان `$1` مسیر یک **فایل موقت** است که پیام داخلشه — هوک پیام را می‌بیند، نه محتوای کامیت را
- این هوک بعد از ساخت پیام اجرا می‌شود؛ رد شدن یعنی کامیت اصلاً ساخته نمی‌شود

این دقیقاً همون چیزیه که در پروژه‌های جدی می‌بینی: پیام‌های ناقص قلقلاق، هیچ‌وقت وارد تاریخچه نمی‌شن.

## ۱۴.۵ — pre-push: آخرین سد قبل از سرور

تست‌ها رو قبل از هر push اجرا کن — تا «رک گول زدن CI» اتفاق نیفته (فصل ۱۵):

```sh
#!/bin/sh
# .git/hooks/pre-push — بدون تست سبز، push ممنوع
npm test --silent || { echo "🚫 تست‌ها رد شدند — push لغو شد"; exit 1; }
```

و یک کاربرد دوستانه‌تر از خانواده‌ی post:

```sh
# .git/hooks/post-merge — بعد از هر pull/merge: وابستگی‌ها تازه باشند
npm install --silent
```

## ۱۴.۶ — هوک در تیم: core.hooksPath و Husky ⭐

چون هوک‌های `.git/hooks` با مخزن سفر نمی‌کنند، برای تیم دو راه داریم:

**راه ۱ — خود گیت:** پوشه‌ای نسخه‌بندی‌شده بساز و گیت را به آن اشاره بده:

```bash
mkdir .githooks
# هوک‌ها را داخل .githooks/ بگذار و کامیت کن؛ سپس هر عضو تیم یک بار:
git config core.hooksPath .githooks
```

**راه ۲ — استاندارد پروژه‌های JS: Husky + lint-staged:**

```bash
npm install --save-dev husky lint-staged
npx husky init                       # .husky/ ساخته می‌شود + core.hooksPath تنظیم می‌شود
echo "npx lint-staged" > .husky/pre-commit
```

```json
// package.json — فقط فایل‌های staged را auto-fix کن
{
  "lint-staged": {
    "*.{js,ts,tsx}": [ "eslint --fix", "prettier --write" ]
  }
}
```

از این به بعد هر کامیت، فقط فایل‌های درگیر را lint و format می‌کند — همون جادویی که وقتی در شرکت کامیت می‌زنی و «auto-fix» می‌شه (فصل ۱۵، جدول ابزارها). اینه عاملش!

## ۱۴.۷ — پرش از هوک: `--no-verify` و اخلاق کار

هر هوک client-side قابل رد شدن است:

```bash
git commit --no-verify -m "wip"     # هوک‌های pre-commit و commit-msg را نمی‌خواند
git push --no-verify                # pre-push را رد می‌زند
```

- 🧘 یک بار در شرایط اضطرار؟ طبیعیه. عادت کردن بهش؟ یعنی هوک‌ت یا بد نوشته شده یا واقعاً لازم نیست — درستش کن، نه این‌که هر روز پرش بزنی
- چون client-side قابل رد شدن و غیرقابل اعتماد برای اعمال *اجباری* است، چک‌های قطعی همیشه **چندلایه**‌اند: هوک محلی (سرعت) + CI روی گیت‌هاب (فصل ۱۵) + protected branch (فصل ۱۱) — دفاع در عمق، نه یک نگهبان تنها

---

## ✅ جمع‌بندی فصل

- هوک = اسکریپت در نقطه‌ای از چرخه گیت؛ exit 0 = ادامه، غیرصفر = لغو
- `pre-commit` محتوا را چک می‌کند (`git diff --cached`)، `commit-msg` پیام را (`$1` = فایل پیام)، `pre-push` آخرین سد است
- هوک‌ها در `.git/hooks` اند و **نسخه‌بندی نمی‌شوند** → برای تیم: `core.hooksPath` یا Husky + lint-staged
- `--no-verify` پرش است، نه راه حل؛ اعمال اجباری همیشه در CI و Rulesets تکرار می‌شود

## 📝 تمرین فصل ۱۴ (همه در زمین تمرین)

1. `pre-commit` بخش ۱۴.۳ را بساز، `chmod +x` بزن، و با یک `.env` staged شده تست کن — خروجی چیست؟ بعد `--no-verify` را امتحان کن.
2. `commit-msg` بخش ۱۴.۴ را نصب کن و با `git commit -m "چیزی کد گذاشتم"` ردش کن؛ بعد با پیام معتبر کامیت موفق بزن.
3. یک `pre-push` بنویس که `git status --porcelain` چک کند — اگر فایل untracked مونده، push رد شود.
4. (چالش) `post-merge` بنویس که تاریخ آخرین pull را در یک فایل `.last-pull` لاگ کند؛ pull بزن و فایل را ببین.

<details><summary>جواب تمرین ۳</summary>

```sh
#!/bin/sh
# .git/hooks/pre-push — push فقط با working directory مرتب
if [ -n "$(git status --porcelain)" ]; then
  echo "🚫 working directory کثیف است (untracked/modified) — اول add/commit یا stash"
  exit 1
fi
```
`git status --porcelain` خروجی قابل‌اسکریپت status است: خالی = تمیز.
</details>

➡️ **فصل بعد:** اتوماسیون سمت گیت‌هاب — GitHub Actions و ابزارهای حرفه‌ای دور گیت؛ جایی که نگهبان‌ها از سیستم تو به سرور مهاجرت می‌کنند.
