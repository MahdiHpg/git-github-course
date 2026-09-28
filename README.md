<div dir="rtl">

# 🎓 دوره جامع Git و GitHub — از «کامیت و پوش بلدم» تا «آماده کار در شرکت»

<div align="center">

[![AI Generated](https://img.shields.io/badge/Generated%20by-GLM--5.3--Flash-blue?style=for-the-badge&logo=openai&logoColor=white)](#)
[![Language](https://img.shields.io/badge/Language-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C-success?style=for-the-badge)](#)
[![Format](https://img.shields.io/badge/Format-PDF%20%2B%20Markdown-orange?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](#)

</div>

> 🤖 **تولید شده توسط هوش مصنوعی:** این دوره به‌طور کامل توسط مدل **GLM-5.3-Flash** تولید و تدوین شده است.
> **نسخه دوره:** ۲۰۲۶ — سازگار با **Git 2.5x** (با اشاره به تغییرات مهم Git 3.0 در راه) و **GitHub فعلی** (Rulesets، GitHub Actions، Fine-grained Token ها)  
> **پیش‌نیاز:** آشنایی مقدماتی با مفاهیم اولیه کامیت و پوش — این دوره از اصول پایه‌ای آغاز کرده و تمامی مهارت‌های پیشرفته مورد نیاز بازار کار را آموزش می‌دهد.

---

## 🎯 چرا این دوره طراحی شده و چه نیازی را پاسخ می‌دهد؟

بسیاری از برنامه‌نویسان در شروع کار، تنها با چند دستور ساده مثل commit و push کار می‌کنند و پروژه‌های خود را روی گیت‌هاب قرار می‌دهند. اما هنگام ورود به تیم‌ها و پروژه‌های بزرگ صنعتی با چالش‌های اساسی روبه‌رو می‌شوند:

- اگر بپرسند «rebase چیست و تفاوت عمیق آن با merge در کجاست؟» پاسخ آماده و دقیقی ندارند
- با **Merge Conflict** روبه‌رو نشده‌اند یا هنگام بروز تعارض، احساس سردرگمی می‌کنند
- روند اصولی ساخت **Pull Request**، کد ریویو (Code Review) و استراتژی‌های ادغام را عملی تجربه نکرده‌اند
- در محیط‌های شرکتی با جریان‌های کاری واقعی (Git Flow، Trunk-based، Protected Branches و CI) روبه‌رو می‌شوند و استانداردهای تیمی را نمی‌دانند

این دوره دقیقاً همین خلاء را پر می‌کند: ارتقای مهارت از یک ابزار ساده «ذخیره کد» به ابزار استاندارد و بین‌المللی «همکاری حرفه‌ای در تیم‌های نرم‌افزاری».

---

## 🗺️ نقشه دوره

| فصل | موضوع | چی یاد می‌گیری |
|---|---|---|
| [فصل ۱](./01-git-why.md) | گیت چیست و چرا | مدل ذهنی درست: snapshot، سه ناحیه، HEAD، SHA |
| [فصل ۲](./02-install-config.md) | نصب و اتصال به گیت‌هاب | نصب ویندوز، **Git Bash**، config، SSH key، توکن |
| [فصل ۳](./03-staging-commits.md) | سه ناحیه و کامیت بامعنا | staging، diff، `git mv`، **کامیت اتمیک**، Conventional Commits |
| [فصل ۴](./04-git-internals.md) | زیر پوست گیت 🕳️ | تور `.git`، آبجکت‌ها (blob/tree/commit)، dedup، index، **git gc** |
| [فصل ۵](./05-git-log.md) | git log حرفه‌ای 🔍 | فیلترها، `main..feature`، **pickaxe**، pretty، shortlog، blame |
| [فصل ۶](./06-undo.md) | برگرداندن‌ها | restore، reset، revert، **reflog** — بدون ترس! |
| [فصل ۷](./07-branches-merge.md) | شاخه‌ها و Merge | branch واقعاً چیه، merge، **حل تعارض** قدم‌به‌قدم |
| [فصل ۸](./08-rebase.md) | Rebase و تاریخچه تمیز | rebase، interactive rebase، squash، قانون طلایی |
| [فصل ۹](./09-stash-tags-ignore.md) | Stash، Tag، gitignore | کمدهای کناری، نسخه‌ها، فایل‌های بی‌خیال، bisect |
| [فصل ۱۰](./10-github-remotes.md) | گیت‌هاب و ریموت‌ها | push/pull/fetch، origin، fork، کلون و SSH |
| [فصل ۱۱](./11-pull-requests.md) | Pull Request و ریویو | PR حرفه‌ای، code review، merge strategies، Rulesets، **Issue** |
| [فصل ۱۲](./12-team-workflows.md) | گردش کار تیمی | GitHub Flow، Git Flow، trunk-based — کی کدوم؟ |
| [فصل ۱۳](./13-rescue-cookbook.md) | کتاب نجات 🚑 | «چه کار کنم اگر...» — ۱۵ سناریوی واقعی شرکت |
| [فصل ۱۴](./14-git-hooks.md) | Git Hooks 🛡️ | pre-commit، commit-msg، pre-push، Husky و lint-staged |
| [فصل ۱۵](./15-actions-tools.md) | GitHub Actions و ابزارها | CI ساده، Checks، Dependabot، امضای کامیت |
| [فصل ۱۶](./16-cheatsheet.md) | چیت‌شیت + گلاساری + مصاحبه | مرور سریع + ۲۴ سوال رایج مصاحبه با جواب |

---

## 🧪 روش مطالعه (خیلی مهم)

این دوره **سرشار از تمرین عملیه** — برای هر فصل یک «زمین تمرین» داریم:

```bash
mkdir git-playground && cd git-playground
git init
```

یک پوشه آزمایشی بسازید و **همه دستورات دوره را آنجا تمرین و اجرا کنید**. اشتباه کردن در محیط آزمایشی کاملاً بی‌خطر و بهترین راه یادگیری است، اما خطا روی مخزن‌های اصلی پروژه هزینه دارد! پاسخ تمرین‌ها درون بخش‌های تاشو قرار داده شده تا ابتدا خودتان راهکار را پیاده‌سازی کنید.

**قانون طلایی دوره:** گیت تقریباً هیچ‌وقت چیزی رو از بین نمی‌بره. تقریباً هر کار اشتباهی برگشت‌پذیره — فصل ۶ و ۱۳ ثابتش می‌کنن. پس ترست رو بذار کنار و تایپ کن.

---

## 📋 پیش‌نیازهای فنی

| ابزار | حداقل | چک کردن |
|---|---|---|
| Windows 10/11 | — | — |
| Git for Windows | 2.4x+ (آخرین نصب کن) | `git --version` |
| حساب GitHub | رایگان | داری ✅ |
| VS Code | توصیه‌شده | ادیتور پیش‌فرض ما |

---

## 📄 تبدیل به PDF

این دوره هم با همون پایپ‌لاین دوره قبلی به PDF رنگی راست‌به‌چپ تبدیل شده. فایل آماده: **«دوره کامل Git و GitHub.pdf»** در همین پوشه. برای بازسازی بعد از ویرایش فصل‌ها:

```bash
python build/build_pdf.py
# سپس رندر با Chrome headless (دستور در build/README)
```

---

## 🏷️ کلمات کلیدی و برچسب‌های سئو (SEO Keywords & Tags)

> **تگ‌های پیشنهادی برای مخزن گیت‌هاب (Topics):**
> `git, github, version-control, git-flow, github-actions, git-commands, persian-tutorial, farsi, آموزش-گیت, آموزش-گیت‌هاب`

**کلمات کلیدی جستجو:**  
آموزش صفر تا صد Git و GitHub فارسی, کتاب آموزش گیت pdf, حل مرج کانفلیکت در گیت, ریبیس و چری پیک گیت, آموزش گیت برای بازار کار, دستورات پرکاربرد git

---

## 📥 دانلود مستقیم نسخه چاپی و PDF کتاب

برای دسترسی و دانلود مستقیم فایل PDF کامل این دوره آموزشی، به بخش **[Releases](../../releases)** همین ریپازیتوری مراجعه کنید یا فایل PDF قرار داده شده در ریشه مخزن را دریافت نمایید.

</div>
