<div align="center">

# ❄ MC88
**🌍 This README is in English and French — scroll down for French ↓**
**🇫🇷 Ce README est en anglais et en français — faites défiler pour le français ↓**
**ثلاث محاولات لنفس الفكرة. لم تنجح أي منها. وكلها هنا.**

</div>

---

<div dir="rtl">

## ما هو هذا المستودع

ليس منتجًا. ليس إصدارًا. ليس مشروعًا يبحث عن نجوم.

إنه **مجلد نجا.**

بين البداية والآن، حاولت أن أجيب على سؤال واحد: *هل يمكن أن يعود الهاتف هاتفًا — بلا وصول، بلا ضجيج خلفي، بلا شبكة لم يطلبها أحد؟*

حاولت ثلاث مرات. كل محاولة علّمتني شيئًا لم تعرفه السابقة. ولا واحدة صارت ما أردت. لكن الثلاث تستحق البقاء، لأن كل واحدة خطوة — حتى تلك التي سارت إلى الوراء.

إن وجدت هذا المستودع مصادفة، فهكذا كنت آمل أن يُوجَد.

إن جئت باحثًا عن شيء محدد، تابع القراءة. ربما تجد القطعة التي كنت تبحث عنها.

إن جئت لتبني على الفكرة، فالقسم الأخير لك.

---

## الملفات الثلاثة

### ١. `os1.html` — المحاكي

المحاولة الأولى. واجهة كاملة تشبه أندرويد، في ملف HTML واحد.

كل شاشة موجودة: الإقلاع، الإعداد، القفل، الرمز السري، الشاشة الرئيسية، درج التطبيقات، التطبيقات الحديثة، اللوحة السريعة، الأذونات، لوحة المفاتيح، ورقة المشاركة، شجرة الإعدادات، المنبهات، الموسيقى، الحاسبة، الكاميرا، المعرض، الملفات، الملاحظات، التقويم، المسجّل، المهملات، المثبّت.

**ما يفعله:** لا شيء على جهازك الحقيقي. كل شيء يجري في المتصفح.

**ما أثبته:** أنني أستطيع تصميم وبناء واجهة نظام تشغيل كامل — وحدي، في ملف واحد، بلا إطار عمل.

**لماذا لم ينجح:** لم يكن صادقًا في أي شيء. بدا كنظام تشغيل. وتصرّف كعرض تجريبي. كل ميزة فيه كانت وهمًا، وأنا كنت أعرف ذلك.

**ما نجا منه:** اللغة البصرية، معمارية ناقل الأحداث، سجل التتبع، نظام الأذونات، لوحة المفاتيح الافتراضية. إن بنيت يومًا واجهة نظام تشغيل حقيقي، فهذا الملف نقطة انطلاقي.

---

### ٢. `deepfreez.html` — لوحة التحكم

المحاولة الثانية. واجهة بصرية لما صار لاحقًا الإصدار الثالث.

ثيم الجليد الداكن. عدّاد ذاكرة حيّ. مفاتيح لخدمات Google، والمرشحين للتجميد، وقيود الجهاز. وزرّ "احذف كل شيء" يعيد الهاتف إلى حالته.

**ما يفعله:** لا شيء. إنه نموذج. كل مفتاح فيه `<div>` بكلاس. وعدّاد الذاكرة عملية حسابية على قيمة ثابتة.

**ما أثبته:** أنني أستطيع تصميم واجهة لأداة لم توجد بعد — وأن أجعلها تبدو وكأنها موجودة.

**لماذا لم ينجح:** كان لوحة تحكم بلا متحكَّم. جهاز تحكم لتلفاز لم يُبنَ قط.

**ما نجا منه:** معمارية الطبقات (طبقة Google، التجميد، القيود، مسار التثبيت، الإزالة)، واللافتة الصادقة التي قالت *"MC88 لا يستطيع إخفاء التطبيقات المجمّدة من مشغّل التطبيقات"*، وتدفّق التأكيد قبل الحذف.

---

### ٣. `v3os.py` — الأداة

المحاولة الثالثة. الوحيدة التي تعمل فعلًا.

ملف Python واحد. يعمل على حاسوبك. يتحدث مع هاتفك عبر `adb`. يسأل سؤالًا واحدًا: **تجميد (Y) أم استعادة (N)؟**

- `Y` — يسجّل ما عليه جهازك الآن، ثم يعطّل التطبيقات التي لا تريدها.
- `N` — يقرأ ذلك السجل، ويعكس كل تغيير، ويعيد الهاتف كما كان.

لا تطبيق مثبّت على الهاتف. لا صلاحيات جذر. لا Device Owner. لا حساب. لا سحابة. لا قياسات.

**ما يفعله:** بالضبط ما يقول. يستخدم فقط أوامر أندرويد الموثّقة (`pm disable-user`، `pm enable`). يكتب سجل JSON قبل كل إجراء. يستعيد بإجابة واحدة.

**ما أثبته:** أن الفكرة *يمكن* أن توجد. لا كنظام تشغيل. لا كتطبيق Device Owner. كسكربت صغير له ذاكرة.

**لماذا لم ينتشر:** كان يحتاج نوعًا معينًا من المستخدمين — شخصًا يعرف أن `adb` موجود، وعنده كابل USB، ومستعد لكتابة أمر واحد.

هذا ليس عددًا كبيرًا. لكنه العدد الصحيح.

**ما نجا منه:** كل شيء. هذا الملف هو السبب الحقيقي لوجود المستودع.

---

## القاعدة الواحدة

الملفات الثلاثة تشترك في قاعدة واحدة، وهي الشيء الوحيد الذي كان يهم:

> **الحالة أولًا. الفعل ثانيًا. السجل هو الذاكرة الوحيدة.**

قبل أن يُلمَس أي شيء، تُكتب حالة الجهاز على القرص. الاستعادة لا تحدث لأن الأداة "تتذكّر". تحدث لأن الأداة *نسيت عن قصد* وتركت ملفًا خلفها.

هذه ليست تفصيلة تقنية. إنها فلسفة. الأداة التي تنسى هي أداة يمكنك الوثوق بها. الأداة التي تتذكّر هي أداة تملكك.

---

## لماذا توقف المشروع

ليس لأنه فشل. بل لأن كل تراجع قرّب الفكرة من شكلها الحقيقي، والثالث كان صحيحًا بالفعل.

- **v1** أراد أن يكون نظام تشغيل. مستحيل على عتاد مغلق.
- **v2** أراد أن يكون تطبيقًا. مقيّد بقواعد المنصة نفسها.
- **v3** أراد أن يكون سكربتًا. صادق.

عندما وُجد v3، لم يبقَ مكان للتراجع. الفكرة بلغت أصغر شكل صحيح لها. وتكبيرها كان سيجعلها أسوأ.

فتوقّف.

ليس من إنهاك. بل احترامًا للشكل الذي اتخذته الفكرة أخيرًا.

---

## ما تعلّمته

**أن "بلا شبكة" ضمان تصميمي، لا ميزة ناقصة.**

**أن القابلية للتراجع ليست مكافأة — بل شرط مسبق ليُسمح لأداة بأن توجد.**

**أن "أبله" مجاملة.** الأداة التي تعرف حدودها أكثر ثقة من التي تتظاهر بأنه لا حدود لها.

**أن معظم الناس لا يريدون هذا.** يريدون هاتفًا يعمل. إزالة Google تعني إزالة نصف الراحة التي دفعوا ثمنها. هذا لا بأس به. لا يجعل الفكرة خاطئة. يجعله لأشخاص أقل.

**أن "لأشخاص أقل" ليس "لا أحد".**

---

## لمن يجد هذا

### إن أردت استخدام v3

ملف Python يعمل. اقرأه. غيّر الإعدادات. أضف إعداداتك. لا يحتاج أي مكتبة خارج المكتبة القياسية.

ستحتاج إلى إنشاء مجلد `profiles/`. الإعداد ملف نصي فيه اسم حزمة في كل سطر، وتعليق اختياري مثل `# network: on` في الأعلى إن أراد الملف تعطيل WiFi و Bluetooth أيضًا.

التعليق في أعلى `v3os.py` يشرح كل شيء.

### إن أردت البناء على الفكرة

ثلاثة اتجاهات تستحق الاستكشاف:

١. **واجهة رسومية حقيقية** لـ v3 — تطبيق سطح مكتب يستدعي السكربت تحته. ملف `deepfreez.html` يظهر اللغة البصرية التي كان في ذهني.

٢. **تطبيق أندرويد حقيقي** باستخدام `DevicePolicyManager` — يُبنى بصدق، كما هو، لا كما يدّعي.

٣. **توثيق حقيقي للفكرة** بالإنجليزية والعربية. الفكرة تستحق أن تُكتب بوضوح، ولم أفعل ذلك أبدًا.

### إن أردت القصة كاملة

إنها في تعليقات الكود. اقرأ `v3os.py` من أعلاه. السطر الأول يقول كل شيء.

---

## ما ليس عليه هذا المستودع

- ليس منتجًا.
- ليس مُصانًا بنشاط.
- ليس نقطة انطلاق لتفريعة تحت الاسم نفسه.

إن بنيت على الفكرة، أخبرني. إن حسّنتها، أخبرني. لكنني لن أدفع تحديثات إلى هذا المجلد.

إنه مجلد. إنه هادئ. إنه هنا لمن يحتاجه.

---

## الترخيص

MIT — للكود.

لكن *الفكرة* — فلسفة الأفعال ذات الحالة أولًا والأدوات القابلة للتراجع — ليست لي لأرخّصها. إنها أقدم من هذا المستودع. خذها. ابنِ عليها. لا تدّعِ أنها بدأت هنا.

</div>

---

<div align="center">

*الهاتف يبقى. الوصول ينتهي.*

<sub>© 2026 محمد الشيخ — MC88</sub>

</div>

<br />
<br />

<div align="center" dir="ltr" style="direction:ltr;text-align:center">

    ███    ███    ████████    ████████    ████████
    ████  ████   ███    ███  ███    ███  ███    ███
    ██ ████ ██   ███         ███    ███  ███    ███
    ██  ██  ██   ███          ████████    ████████
    ██      ██   ███         ███    ███  ███    ███
    ██      ██   ███    ███  ███    ███  ███    ███
    ██      ██    ████████    ████████    ████████

</div>
<div align="center">

# ❄ MC88

**Three attempts at the same idea. None of them landed. All of them are here.**

</div>

---

## What this repository is

Not a product. Not a release. Not a project looking for stars.

It's a **folder that survived.**

Between the beginning and now, I tried to answer one question: *can a phone be a phone again — without the reach, without the background noise, without the network it never asked for?*

I tried three times. Each attempt taught me something the previous one couldn't. None of them became what I wanted. But all three are worth keeping, because each one is a step — even the ones that walked backward.

If you found this repository by accident, that's how I hoped it would be found.

If you came searching for something specific, read on. You might find the piece you were looking for.

If you came to build on this idea, the last section is for you.

---

## The three files

### 1. `os1.html` — the simulator

The first attempt. A complete Android-like interface in one HTML file.

Every screen exists: boot, setup, lock, PIN, home, app drawer, recents, quick panel, permissions, keyboard, share sheet, settings tree, alarms, music, calculator, camera, gallery, files, notes, calendar, recorder, trash, installer.

**What it does:** nothing on your actual device. Everything runs in the browser.

**What it proved:** I could design and build an entire operating system's interface — alone, in one file, without a framework.

**Why it didn't land:** it was honest about nothing. It looked like an OS. It behaved like a demo. Every feature was fake, and I knew it.

**What survives from it:** the visual language, the event-bus architecture, the audit log, the permission system, the virtual keyboard. If I ever build a real phone OS interface, this file is my starting point.

---

### 2. `deepfreez.html` — the control panel

The second attempt. A visual front-end for what became v3.

Dark ice theme. Live RAM counter. Toggles for Google services, freeze candidates, device restrictions. A "remove everything" button that would restore the phone.

**What it does:** nothing. It's a mockup. Every toggle is a `<div>` with a class. The RAM counter is arithmetic on a constant.

**What it proved:** I could design an interface for a tool that didn't exist yet — and make it feel like it did.

**Why it didn't land:** it was a control panel without a controller. A remote for a TV that was never built.

**What survives from it:** the layered information architecture (Google Layer / Freeze / Restrictions / Install Path / Removal), the honest banner that said *"MC88 cannot hide frozen apps from your launcher"*, the confirmation flow.

---

### 3. `v3os.py` — the tool

The third attempt. The one that actually works.

A single Python file. Runs on your computer. Talks to your phone over `adb`. Asks one question: **Freeze (Y) or Restore (N)?**

- `Y` — records what your device is, then disables the apps you don't want.
- `N` — reads that record back, reverses every change, returns the phone to how it was.

No app installed on the phone. No root. No Device Owner. No account. No cloud. No telemetry.

**What it does:** exactly what it says. Uses only documented Android commands (`pm disable-user`, `pm enable`). Writes a JSON log before every action. Restores in one answer.

**What it proved:** the idea *can* exist. Not as an OS. Not as a Device Owner app. As a small script with a memory.

**Why it didn't spread:** it required a specific kind of user — someone who knows `adb` exists, who has a USB cable, who's willing to type one command.

That's not many people. But it's the right people.

**What survives from it:** everything. This is the file the repository is actually for.

---

## The one rule

All three files share one rule, and it's the only thing that mattered:

> **State first. Action second. The log is the only memory.**

Before anything is touched, the state of the device is written to disk. Restoration doesn't happen because the tool "remembers." It happens because the tool *forgot on purpose* and left a file behind.

That's not a technical detail. It's a philosophy. A tool that forgets is a tool you can trust. A tool that remembers is a tool that owns you.

---

## Why the project stopped

Not because it failed. Because each retreat brought the idea closer to its true shape, and the third one was already correct.

- **v1** wanted to be an operating system. Impossible on closed hardware.
- **v2** wanted to be an app. Constrained by the platform's own rules.
- **v3** wanted to be a script. Honest.

Once v3 existed, there was nowhere left to retreat to. The idea had reached its smallest true form. Making it bigger would have made it worse.

So it stopped.

Not out of exhaustion. Out of respect for the shape the idea had finally taken.

---

## What I learned

**That "no network" is a design guarantee, not a missing feature.**

**That reversibility is not a bonus — it's a precondition for a tool to be allowed to exist.**

**That "dumb" is a compliment.** A tool that knows its limits is more trustworthy than one that pretends to have none.

**That most people don't want this.** They want a phone that works. Removing Google means removing half the convenience they paid for. That's fine. It doesn't make the idea wrong. It makes it for a smaller number of people.

**That "for a smaller number of people" is not "for nobody."**

---

## For whoever finds this

### If you want to use v3

The Python file works. Read it. Change the profiles. Add your own. It has no dependencies outside the standard library.

You'll need to create a `profiles/` folder. A profile is a text file with a package name per line, and an optional comment like `# network: on` at the top if the profile should also turn off WiFi and Bluetooth.

The header comment at the top of `v3os.py` walks you through it.

### If you want to build on the idea

Three directions worth exploring:

1. **A real GUI wrapper** for v3 — a desktop app that calls the Python script underneath. `deepfreez.html` shows the visual language I had in mind.
2. **A proper Android app** using `DevicePolicyManager` — built honestly, as what it is, not as what it claims to be.
3. **Proper documentation of the concept** in both English and Arabic. The idea deserves to be written down clearly, and I never got to it.

### If you want the whole story

It's in the code comments. Read `v3os.py` from the top. The header says everything.

---

## What this repository is not

- Not a product.
- Not actively maintained.
- Not a starting point for a fork under the same name.

If you build on the idea, tell me. If you make it better, tell me. But I won't be pushing updates to this folder.

It's a folder. It's quiet. It's here for whoever needs it.

---

## License

MIT — for the code.

But the *idea* — the philosophy of state-first actions and reversible tools — isn't mine to license. It's older than this repository. Take it. Build on it. Don't pretend it started here.

---

<div align="center">

*The phone stays. The reach ends.*

<sub>© 2026 Mohamed Cheikh — MC88</sub>

<br />
<br />

    ███    ███    ████████    ████████    ████████
    ████  ████   ███    ███  ███    ███  ███    ███
    ██ ████ ██   ███         ███    ███  ███    ███
    ██  ██  ██   ███          ████████    ████████
    ██      ██   ███         ███    ███  ███    ███
    ██      ██   ███    ███  ███    ███  ███    ███
    ██      ██    ████████    ████████    ████████

</div>
<div align="center">

# ❄ MC88

**Trois tentatives pour la même idée. Aucune n'a abouti. Toutes sont ici.**

</div>

---

## Ce qu'est ce dépôt

Pas un produit. Pas une release. Pas un projet en quête d'étoiles.

C'est un **dossier qui a survécu.**

Entre le début et maintenant, j'ai essayé de répondre à une seule question : *un téléphone peut-il redevenir un téléphone — sans la portée, sans le bruit de fond, sans le réseau qu'il n'a jamais demandé ?*

J'ai essayé trois fois. Chaque tentative m'a appris quelque chose que la précédente ignorait. Aucune n'est devenue ce que je voulais. Mais toutes méritent de rester, parce que chacune est une étape — même celles qui reculaient.

Si vous êtes tombé sur ce dépôt par hasard, c'est ainsi que j'espérais qu'il soit trouvé.

Si vous cherchiez quelque chose de précis, continuez à lire. Vous trouverez peut-être la pièce qu'il vous manquait.

Si vous êtes venu pour bâtir sur l'idée, la dernière section est pour vous.

---

## Les trois fichiers

### 1. `os1.html` — le simulateur

La première tentative. Une interface complète qui ressemble à Android, dans un seul fichier HTML.

Chaque écran existe : démarrage, configuration, verrouillage, code PIN, écran d'accueil, tiroir d'applications, applications récentes, panneau rapide, permissions, clavier, feuille de partage, arbre de réglages, alarmes, musique, calculatrice, appareil photo, galerie, fichiers, notes, calendrier, enregistreur, corbeille, installateur.

**Ce qu'il fait :** rien sur votre appareil réel. Tout se passe dans le navigateur.

**Ce qu'il a prouvé :** que je pouvais concevoir et construire l'interface complète d'un système d'exploitation — seul, dans un seul fichier, sans framework.

**Pourquoi il n'a pas abouti :** il n'était honnête sur rien. Il ressemblait à un OS. Il se comportait comme une démo. Chaque fonctionnalité était un simulacre, et je le savais.

**Ce qui en survit :** le langage visuel, l'architecture de bus d'événements, le journal d'audit, le système de permissions, le clavier virtuel. Si un jour je construis une vraie interface d'OS mobile, ce fichier sera mon point de départ.

---

### 2. `deepfreez.html` — le panneau de contrôle

La deuxième tentative. Une interface visuelle pour ce qui allait devenir la v3.

Thème de glace sombre. Compteur de RAM en direct. Interrupteurs pour les services Google, les candidats au gel, les restrictions de l'appareil. Un bouton « tout retirer » qui restaurerait le téléphone.

**Ce qu'il fait :** rien. C'est une maquette. Chaque interrupteur est un `<div>` avec une classe. Le compteur de RAM est une arithmétique sur une constante.

**Ce qu'il a prouvé :** que je pouvais concevoir l'interface d'un outil qui n'existait pas encore — et lui donner l'air d'exister.

**Pourquoi il n'a pas abouti :** un panneau de contrôle sans contrôleur. Une télécommande pour une télévision jamais construite.

**Ce qui en survit :** l'architecture d'information par couches (couche Google, gel, restrictions, chemin d'installation, retrait), la bannière honnête qui disait *« MC88 ne peut pas masquer les applications gelées du lanceur »*, le flux de confirmation.

---

### 3. `v3os.py` — l'outil

La troisième tentative. La seule qui fonctionne vraiment.

Un seul fichier Python. Tourne sur votre ordinateur. Parle à votre téléphone via `adb`. Pose une seule question : **Geler (Y) ou restaurer (N) ?**

- `Y` — enregistre l'état de l'appareil, puis désactive les applications dont vous ne voulez plus.
- `N` — relit cet enregistrement, inverse chaque changement, rend le téléphone tel qu'il était.

Aucune application installée sur le téléphone. Pas de root. Pas de Device Owner. Pas de compte. Pas de cloud. Pas de télémétrie.

**Ce qu'il fait :** exactement ce qu'il dit. Utilise uniquement des commandes Android documentées (`pm disable-user`, `pm enable`). Écrit un journal JSON avant chaque action. Restaure en une seule réponse.

**Ce qu'il a prouvé :** que l'idée *peut* exister. Pas comme un OS. Pas comme une application Device Owner. Comme un petit script avec une mémoire.

**Pourquoi il ne s'est pas répandu :** il exigeait un type particulier d'utilisateur — quelqu'un qui sait que `adb` existe, qui possède un câble USB, qui accepte de taper une commande.

Ce n'est pas beaucoup de gens. Mais ce sont les bonnes personnes.

**Ce qui en survit :** tout. C'est le fichier pour lequel ce dépôt existe réellement.

---

## La règle unique

Les trois fichiers partagent une seule règle, et c'est la seule chose qui comptait :

> **L'état d'abord. L'action ensuite. Le journal est la seule mémoire.**

Avant que quoi que ce soit ne soit touché, l'état de l'appareil est écrit sur le disque. La restauration n'a pas lieu parce que l'outil « se souvient ». Elle a lieu parce que l'outil *a oublié exprès* et a laissé un fichier derrière lui.

Ce n'est pas un détail technique. C'est une philosophie. Un outil qui oublie est un outil en qui vous pouvez avoir confiance. Un outil qui se souvient est un outil qui vous possède.

---

## Pourquoi le projet s'est arrêté

Pas parce qu'il a échoué. Parce que chaque recul rapprochait l'idée de sa vraie forme, et la troisième était déjà correcte.

- **v1** voulait être un système d'exploitation. Impossible sur un matériel fermé.
- **v2** voulait être une application. Contraint par les règles de la plateforme elle-même.
- **v3** voulait être un script. Honnête.

Une fois v3 existant, il n'y avait plus nulle part où reculer. L'idée avait atteint sa plus petite forme vraie. L'agrandir l'aurait rendue pire.

Alors elle s'est arrêtée.

Pas par épuisement. Par respect pour la forme qu'elle avait enfin prise.

---

## Ce que j'ai appris

**Que « pas de réseau » est une garantie de conception, pas une fonctionnalité manquante.**

**Que la réversibilité n'est pas un bonus — c'est une condition préalable pour qu'un outil soit autorisé à exister.**

**Que « bête » est un compliment.** Un outil qui connaît ses limites est plus digne de confiance qu'un outil qui prétend n'en avoir aucune.

**Que la plupart des gens ne veulent pas ça.** Ils veulent un téléphone qui marche. Retirer Google revient à retirer la moitié du confort qu'ils ont payé. Ce n'est pas grave. Ça ne rend pas l'idée fausse. Ça la rend destinée à un plus petit nombre.

**Que « un plus petit nombre » n'est pas « personne ».**

---

## Pour qui trouve ceci

### Si vous voulez utiliser v3

Le fichier Python fonctionne. Lisez-le. Modifiez les profils. Ajoutez les vôtres. Il n'a aucune dépendance hors de la bibliothèque standard.

Vous devrez créer un dossier `profiles/`. Un profil est un fichier texte avec un nom de paquet par ligne, et un commentaire optionnel comme `# network: on` en tête si le profil doit aussi couper le WiFi et le Bluetooth.

Le commentaire en haut de `v3os.py` vous guide pas à pas.

### Si vous voulez bâtir sur l'idée

Trois directions valent l'exploration :

1. **Une véritable interface graphique** pour v3 — une application de bureau qui appelle le script Python en dessous. `deepfreez.html` montre le langage visuel que j'avais en tête.
2. **Une vraie application Android** utilisant `DevicePolicyManager` — construite honnêtement, pour ce qu'elle est, pas pour ce qu'elle prétend être.
3. **Une vraie documentation du concept**, en anglais et en arabe. L'idée mérite d'être écrite clairement, et je ne l'ai jamais fait.

### Si vous voulez l'histoire complète

Elle est dans les commentaires du code. Lisez `v3os.py` depuis le début. L'en-tête dit tout.

---

## Ce que ce dépôt n'est pas

- Pas un produit.
- Pas activement maintenu.
- Pas un point de départ pour un fork sous le même nom.

Si vous bâtissez sur l'idée, dites-le-moi. Si vous l'améliorez, dites-le-moi. Mais je ne pousserai pas de mises à jour dans ce dossier.

C'est un dossier. Il est silencieux. Il est là pour qui en a besoin.

---

## Licence

MIT — pour le code.

Mais l'*idée* — la philosophie des actions « état d'abord » et des outils réversibles — n'est pas à moi à licencier. Elle est plus ancienne que ce dépôt. Prenez-la. Bâtissez dessus. Ne prétendez pas qu'elle a commencé ici.

---

<div align="center">

*Le téléphone reste. La portée s'arrête.*

<sub>© 2026 Mohamed Cheikh — MC88</sub>

<br />
<br />

    ███    ███    ████████    ████████    ████████
    ████  ████   ███    ███  ███    ███  ███    ███
    ██ ████ ██   ███         ███    ███  ███    ███
    ██  ██  ██   ███          ████████    ████████
    ██      ██   ███         ███    ███  ███    ███
    ██      ██   ███    ███  ███    ███  ███    ███
    ██      ██    ████████    ████████    ████████

</div>
