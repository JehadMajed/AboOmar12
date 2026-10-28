# مراجعة تقنية لعرض Radio over Fiber (RoF)

**الملف الأصلي:** `Radio_over_Fiber_Reviewed_Final_v4.pptx`، ويضم 31 شريحة و5 صور نقطية (Raster).
**المخرجات:**
- `RoF_Technical_Review.pptx`: العرض المعاد بناؤه، ويضم 13 شريحة رئيسية و8 شرائح Appendix. كل الرسوم فيه Vector أصلية قابلة للتحرير، وليس فيه صور نقطية.
- `build_rof_deck.js`: السكربت الذي يولّد العرض.
- هذا التقرير.

**قيود التحقق:** تعذّر الوصول من بيئة العمل إلى arxiv.org وmdpi.com وpbeaxell.com. لذلك وُسمت كل قيمة تعتمد على هذه المصادر وحدها بعبارة *Verification required*. تحققتُ مباشرة من القيم التالية:
- توهين LMR-400، وهو 22.2 dB/100 m عند 2500 MHz.
- تواريخ إصدارات G.Suppl.55، وآخرها 10/2025.
- وقائع حالة الملاعب كما وردت في بيانات Axell وRFS الصحفية لعام 2014.

---

## A. المشكلات التقنية والمنطقية مرتبة حسب الخطورة

1. **نسبة خصائص الـFiber إلى النظام كله.** تكرر العرض بأن "الألياف منخفضة الفقد" دون احتساب فقد التحويل E/O وO/E، وهو فقد ثابت لا يعتمد على الطول. تكرر ذلك في الشرائح 3 و14 و15 و16 و29. النتيجة مقارنة غير صحيحة لأداء الوصلة RF-to-RF.
2. **جدول الفقد (الشريحة 16) يقارن كابلًا بكابل.**
   - يقارن 22 dB/100 m للـCoax بـ0.2 dB/km للـFiber، ثم يستنتج أن "2,200 dB ... more than any amplifier could recover".
   - الاستقراء الخطي إلى 10 km لا يمثل نظامًا يُبنى فعلًا. أنظمة Coax الطويلة، مثل HFC، تستخدم مكبرات على طول الخط.
   - المقارنة الصحيحة تكون بين وصلتين كاملتين، مع إدراج فقد التحويل Lc.
3. **خطأ تصنيفي في عنوان الشريحة 12: "Benefits of RoF vs. Traditional Wireless".** RoF ليس بديلًا للاتصال اللاسلكي، بل وسيلة نقل لإشارة لاسلكية. أساس المقارنة غير محدد.
4. **خلط Transport Capacity بـWireless Capacity** في الشرائح 12 و18 و22. أُضيفت ملاحظات تصحيحية، لكن العبارة الأصلية ("Increased capacity", "High capacity transport ... supporting many users") بقيت قائمة.
5. **تناقض في موضع الـPhotodiode.** الشريحة 11 تقول "at the base station"، والشرائح 4 و5 و8 تقول "at the remote unit". كذلك يسمّي الرسم الأصلي (image2) طرف الاستقبال "Base Station".
6. **تقديم WDM كأنه جزء أساسي من الوصلة.** الرسم الأصلي للـBlock Diagram يضع MUX/DEMUX في المسار الرئيسي، وتُدرج الشريحة 11 الـMUX/DEMUX ضمن "Key Building Blocks". في الواقع WDM اختياري.
7. **وصف الـRemote Unit بأنه "very simple" أو "the simplest"** في الشريحتين 9 و10 دون تحديد المعمارية. حتى في RFoF تحتوي الـRAU على PD وTIA وPA وLNA وLD وDuplexer ومصدر تغذية.
8. **تناقض داخلي:** "Flexibility and scalability" في الشريحة 19 مقابل "Limited flexibility: each antenna node needs a dedicated fiber" في الشريحة 24. وتتعارض الأخيرة أيضًا مع ما يقوله العرض عن WDM.
9. **خلط RRH بـRAU** في جدول المصطلحات (الشريحة 6: "RRH / RAU" بمعنى واحد). الـRRH وحدة راديو كاملة فيها DAC/ADC وتُغذّى بـDigital Fronthaul. الـRAU وحدة وصلة تماثلية.
10. **خلط Digital RoF بـCPRI** (الشريحة 10). CPRI مواصفة صناعية وليست معيار ITU-T. كما أن معدل eCPRI لا يتناسب مع عدد الهوائيات بالطريقة نفسها.
11. **مقارنة مع Microwave link (الشريحة 15) من فئة وظيفية مختلفة.** الـMicrowave link وصلة Backhaul من نقطة إلى نقطة، بينما RoF وصلة تغذية هوائي. لم تُحدد نقطتا الإرسال والاستقبال ولا نوع الإشارة.
12. **رسم المعمارية الأصلي (image)** يخلط بين C-RAN (BBU Pool وRRH)، وPON (Splitter وOptical Access Network)، وBackhaul/Fronthaul بأسهم غامضة. ولا يبيّن نوع الإشارة على أي وصلة.
13. **رسم DAS الأصلي (image4)** منخفض الدقة. فيه "CU" غير معرّف، ولا يبيّن نوع الإشارة ولا موضع التحويل.
14. **الـBlock Diagram الأصلي (image2)** يضع "RF Modulator" قبل الـMZM، وهو تكرار وظيفي لأن الـMZM نفسه هو المعدِّل. ويغيب عنه الـAmplifier المذكور في النص، ولا يظهر فيه الـUplink.
15. **حالة الملاعب (الشريحة 21):**
    - المورد المذكور (RFS) غير دقيق في نسبته. بحسب البيانات الصحفية زوّدت Axell Wireless نظام Optical DAS، وزوّدت RFS كابل HYBRIFLEX في Maracanã.
    - تاريخ نشر الـCase Study وأسماء المعدات (OMU Mk. II) لم أتمكن من التحقق منها.
16. **منحنى CSR (الشريحة 26):**
    - القيم مقروءة تقريبيًا من رسم منشور.
    - قيمة −log10(BER) ≈ 2، أي BER ≈ 1e-2، أعلى من عتبة HD-FEC الشائعة (≈ 3.8e-3). لم يُذكر ذلك.
    - موضعه في العرض الرئيسي لا يخدم الحجة، فنُقل إلى الـAppendix.
17. **شريحة 6G (الشريحة 27):** عرض بحثي بعبارة "optional for beginners"، وهي نبرة غير مناسبة للجنة. نُقلت إلى الـAppendix.
18. **قيمة 0.2 dB/km تحتاج تأهيلًا.** هي قيمة نموذجية للألياف. أما الـDatasheets الحالية لكوابل G.652.D فتعطي حدًا أقصى بين 0.22 و0.25 dB/km عند 1550 nm. استخدمتُ 0.25 dB/km كقيمة محافظة.
19. **أرقام Li et al. (40× وEVM 8%)** صحيحة الإطار كنتائج نمذجة خاصة بسيناريو محدد. لكن تعذّر التحقق منها من النص الكامل، فوُسمت بـVerification required.
20. **مشكلات النبرة والبنية:**
    - أسئلة استعراضية، مثل "How do you bring a clear mobile signal inside a tunnel…?".
    - عبارات مثل "In plain words" و"Still tiny next to coax".
    - تكرار الـDAS في 4 شرائح.
    - غياب فصل واضح بين المتحدثين وغياب توزيع زمني.
    - 31 شريحة لعرض مدته 15 دقيقة.
21. **المصدر الأساسي فيديو (SolFinder Research)**، وهو مصدر ثانوي لا يصلح أساسًا لادعاء تقني أمام لجنة. لم يُستند إليه في النسخة الجديدة.

---

## B. جدول الادعاءات

التصنيف: **S** = Supported، **Q** = Requires qualification، **U** = Unsupported، **X** = Technically incorrect.

| # | Original Claim (الشريحة) | التصنيف | Issue | Revised Claim | Evidence Needed |
|---|---|---|---|---|---|
| 1 | "Optical fiber loses very little signal… This is the idea behind RoF." (3) | Q | يتجاهل فقد التحويل E/O وO/E | Fiber attenuation is low (≈0.2–0.25 dB/km at 1550 nm); RF-to-RF loss of an RoF link = Lc + 2×optical loss | G.652.D datasheets؛ Cox (2004)؛ Datasheet الجهاز لقيمة Lc |
| 2 | "Coaxial cable… loses signal quickly over distance and is heavy and bulky." (3) | Q | لا تُحدد الكلام بتردد أو نوع كابل | LMR-400-class coax: 22.2 dB/100 m at 2.5 GHz | Times Microwave LMR-400 datasheet ✔ |
| 3 | "RoF carries RF or IF…" (4) | S | — | يبقى كما هو، مع فصل Digital fronthaul صراحة | ITU-T G.Suppl.55 |
| 4 | "Photodiode: converts the light back… at the base station." (11) | X | الـPD في الـDownlink موجود في الـRAU | O/E (photodiode) is at the RAU for downlink and at the central site for uplink | — |
| 5 | "WDM can combine several optical channels" + MUX/DEMUX في الرسم الأساسي (5، 8، 11) | Q | يوحي بأن WDM جزء أساسي | WDM is optional; required only when several links share one fiber | ITU-T G.Suppl.55 |
| 6 | "RFoF: …the simplest RAU." (9) | Q | البساطة نسبية، والوحدة تبقى نشطة | RFoF RAU has no frequency conversion, but contains PD, TIA, PA, LNA, LD and power supply | Electronics 9(11) 1785, Fig. 3 |
| 7 | "Remote unit: Very simple: photodiode, filter, amplifier" (10) | X | يغفل الـUplink والـDuplexer والتغذية | O/E, E/O, amplifiers, filters (+ mixer and LO for IFoF) | — |
| 8 | "Fiber bandwidth: Efficient" vs "Very high" (10) | U | وصف غير كمي | Analog ≈ channel bandwidth per stream; CPRI = fs×2×N×16/15×line code (1228.8 Mb/s for 20 MHz LTE) | CPRI V7.0 ✔ (حساب) |
| 9 | "Standards: …CPRI / eCPRI" مقابل ITU-T (10) | Q | CPRI مواصفة صناعية وليست معيار ITU | CPRI/eCPRI: industry specifications; G.9803: ITU-T system requirements | CPRI/eCPRI specs؛ ITU-T |
| 10 | "Benefits of RoF vs. Traditional Wireless" (12) | X | خطأ تصنيفي: RoF ليس بديلًا للاتصال اللاسلكي | حُذف العنوان، وحلت محله "Benefits, and the conditions under which they hold" | — |
| 11 | "Extended coverage: …one central site can serve a much larger area." (12) | Q | التغطية تحددها مواقع الهوائيات، والألياف تحدد المسافة إلى المركز فقط | Fiber allows antenna points to be placed far from the central equipment | — |
| 12 | "Increased capacity: fiber has far more bandwidth than copper or radio links" (12) | X | يخلط Transport Capacity بـWireless Capacity، والسعة في A-RoF تحددها الـOptoelectronics والـDynamic range | RoF moves the radiation point; it does not add spectrum or air-interface capacity | — |
| 13 | "Cost efficiency: RoF can reuse existing fiber…" (13) | Q | A-RoF يحتاج عادة ليفًا أو طول موجة مخصصًا، والتكلفة تختلف من موقع لآخر | Cost advantage is site-specific; not established | BoM لموقع محدد – Verification required |
| 14 | "Low attenuation: …around 0.2 dB/km at 1550 nm" (14) | Q | قيمة نموذجية، لا حد أقصى معياري | ≤0.22–0.25 dB/km cabled (vendor datasheets) | Prysmian/Datwyler/Leviton G.652.D ✔ |
| 15 | "Fewer active parts at remote sites…" (14) | Q | يعتمد على المعمارية | True for RFoF/IFoF relative to an RRH | — |
| 16 | "A transparent optical link can carry different radio standards" (14) | Q | محدود بالـBandwidth والـLinearity والـDynamic range، ولا يصح في CPRI | Within optoelectronic bandwidth, linearity and dynamic range | Cox (2004) |
| 17 | جدول Coax / Microwave / RoF (15) | X | فئات وظيفية مختلفة، ولا نقاط طرفية محددة، و"Reach: many km" دون شرط dispersion/noise | Comparison 1 (coax vs RFoF، نقاط وإشارة ومعيار وافتراضات محددة) | — |
| 18 | "10 km: 2,200 dB… more than any amplifier could recover" (16) | X | استقراء لنظام لا يُبنى، وتجاهل المكبرات على الخط | Passive coax is impractical at these lengths; values are extrapolations | — |
| 19 | "1 dB optical → ~2 dB RF" (16) | S | — | يبقى، مع شرط IM/DD | Cox (2004) |
| 20 | "Better coverage: reaches places hard to cover…" (18) | Q | ميزة DAS لا ميزة RoF (Passive coax DAS يحققها أيضًا) | RoF is a transport choice inside a DAS | — |
| 21 | "Each antenna node needs a dedicated fiber link" (24) | Q | يتناقض مع WDM والـCascading | Star topology by default; WDM or cascaded RAUs reduce fiber count | ITU-T G.Suppl.55 |
| 22 | "Equipment supplier: RFS" (21) | Q | بحسب البيانات الصحفية: Axell قدّمت Optical DAS، وRFS قدّمت كابل HYBRIFLEX في Maracanã | Axell Wireless (optical DAS); RFS (HYBRIFLEX, Maracanã) | Axell PR 06/2014 ✔؛ RFS PR 10/06/2014 ✔ |
| 23 | "OMU Mk. II…", "published 14 Nov 2024" (21) | U | تعذّر الوصول إلى الصفحة | Optical master units (model names: Verification required) | pbeaxell.com – Verification required |
| 24 | "combined capacity over 141,000" (21) | S | — | يبقى | Axell PR 06/2014 ✔ |
| 25 | "5G fronthaul… suited to dense small cells and mmWave" (22) | Q | الـFronthaul التجاري لـ5G رقمي في الغالب (CPRI/eCPRI/O-RAN 7.2x)، وA-RoF لـ5G في مرحلة بحث وتجارب | A-RoF fronthaul: G.9803 Amd. 2 requirements; mostly research/trials | ITU-T G.9803 Amd. 2 – Verification required for deployment status |
| 26 | "Loss and dispersion… dispersion compensation" (23) | Q | يغفل الآلية الخاصة بـRoF | DSB intensity modulation → dispersion-induced RF power fading; mitigations: 1310 nm, SSB, IFoF | Gliese et al. 1996 |
| 27 | "analogue RoF ≈ 8% EVM vs 3.5% target" (25) | Q | نتيجة نمذجة. قيمة 3.5% مؤكدة (3GPP)، أما قيمة 8% فلم يُتحقق منها | Moved to A6 with flag | TS 38.104 ✔؛ Li et al. – Verification required |
| 28 | "up to 40× lower fiber bandwidth" (28) | Q | خاص بسيناريو نمذجة واحد | Moved to A6 with scenario stated | Li et al. – Verification required |
| 29 | "BER improves as CSR rises to ~25 dB" (26) | Q | قراءة تقريبية من رسم منشور، والقيم المنخفضة فوق عتبة FEC | Moved to A4 with limits | Hadi & Murtaza 2023 Fig. 6 – Verification required |
| 30 | "Silicon photonics could… reduce device cost" (28) | U | تنبؤ بلا دليل كمي | حُذف من العرض الرئيسي | — |
| 31 | "Fiber is lightweight and flexible…" (14) | S | — | Small, light cable compared with coax of similar loss | — |
| 32 | "G.Suppl.55 (2025)" (31) | S | التاريخ الدقيق 10/2025 | G.Suppl.55 (10/2025) | ITU-T ✔ |

---

## C. الهيكل الجديد مع توزيع الوقت والمتحدثين

| # | الشريحة | الوظيفة | المتحدث | الوقت | التراكمي |
|---|---|---|---|---|---|
| 1 | Title | تحديد الموضوع وتقسيم الأدوار | A | 0:20 | 0:20 |
| 2 | Problem and scope | المشكلة، وحدود النطاق، والبدائل | A | 1:15 | 1:35 |
| 3 | Definition | تعريف وضبط المصطلحات | A | 1:15 | 2:50 |
| 4 | End-to-end signal path | DL/UL، ومواضع E/O وO/E، وقاعدة 1 dB→2 dB | A | 1:45 | 4:35 |
| 5 | Architecture | موضع الوصلة، والفرق بين Fronthaul وBackhaul | A | 1:30 | 6:05 |
| 6 | RoF types | RFoF/IFoF/Digital، ومقايضة التعقيد مقابل السعة | A | 1:30 | 7:35 |
| — | **تسليم إلى المتحدث B** | | | 0:10 | 7:45 |
| 7 | Comparison 1 | Coax مقابل RFoF، وطول التعادل | B | 1:45 | 9:30 |
| 8 | Comparison 2 | A-RoF مقابل CPRI | B | 1:30 | 11:00 |
| 9 | Benefits + conditions | الفائدة، وشرطها، وما لا تعنيه | B | 1:00 | 12:00 |
| 10 | Limitations | الآليات الفيزيائية وSFDR | B | 1:15 | 13:15 |
| 11 | Documented case | حالة موثقة، وما تثبته وما لا تثبته | B | 1:00 | 14:15 |
| 12 | Conclusions | استنتاجات مربوطة بالأدلة | B | 0:45 | 15:00 |
| 13 | Questions | — | A+B | — | — |
| A1–A8 | Appendix | مرجعي، للأسئلة | — | — | — |

---

## D وE. نص الشرائح وSpeaker Notes

النص الإنجليزي الكامل لكل شريحة وملاحظات المتحدث موجودان داخل ملف `RoF_Technical_Review.pptx`، كلٌّ في Notes الشريحة الخاصة بها. أُلحقت نسخة نصية مستخرجة آليًا منهما في نهاية هذا التقرير (الملحق: Slide text and notes)، لتكون مرجعًا واحدًا لا يتعارض مع الملف.

مبدأ الـNotes: كل ملاحظة تشرح منطق الشريحة وحدود ادعائها، وتعطي الحساب أو المصدر عند الحاجة. لا تكرر نص الشريحة.

---

## F. تعليمات التصميم لكل رسم وجدول

**قواعد عامة طُبّقت في كل الشرائح**

- **الخلفية والألوان:** خلفية بيضاء. نص أسود (1A1A1A). العناوين Navy (1F3A5F).
- **رموز المسارات:**
  - المسار الكهربائي: خط أسود رفيع (1.25 pt).
  - المسار الضوئي: خط Navy سميك (3 pt).
  - المسار اللاسلكي: خط رمادي متقطع.
- **كتل التحويل:** كتل E/O وO/E وحدها مملوءة بالأزرق الفاتح (DCE6F2). بذلك يظهر موضع التحويل دون نص إضافي.
- **مفتاح الرموز:** على كل رسم Legend للمسارات.
- **الخطوط:** Calibri لكل النصوص. العنوان 28 pt. النص 13–14 pt. الجداول 12–14 pt. المصادر 10 pt.
- **ما لم يُستخدم:** لا Gradients، ولا صور Stock، ولا زخارف، ولا خطوط تحت العناوين.
- **المصادر:** كل شريحة تحمل سطر مصدر في أسفلها.

**تعليمات خاصة بكل رسم وجدول**

| الشريحة | العنصر | التعليمات |
|---|---|---|
| 1 | شريط تخطيطي | Central → E/O → Fiber → O/E → RAU → Air → UE. يُكتب نوع الإشارة على الوصلة الضوئية |
| 2 | مخطط النطاق | Core –Backhaul (digital, packet)→ Central → [منطقة مظللة: Transport segment] → Remote points ~Air~> UE. يُذكر صراحة أن اتجاه الـDL هو المعروض |
| 3 | جدول المصطلحات | عمودان (Term \| Meaning). صف الترويسة بخلفية رمادية فاتحة. ست مفاهيم متمايزة |
| 4 | Signal path | منطقتان متقطعتان (Central site وRAU) وبينهما الـFiber. صف DL من اليسار إلى اليمين، وصف UL من اليمين إلى اليسار. الـDuplexer يمتد على الصفين. على الوصلة الضوئية: "intensity-modulated, λ1" و"λ2 or second fiber". تحت الرسم ثلاث خلايا: نقاط التحويل، وقاعدة 1 dB→2 dB، وأن WDM اختياري |
| 5 | Architecture | BS hotel (3 مشغلين) → RF coax → Head-end (E/O وO/E) → نجمة ألياف ثنائية الاتجاه → RAU 1..n، والـRAU n متقطع. Backhaul معنون. لوحة جانبية تفصل Fronthaul عن Backhaul |
| 6 | Types | ثلاثة صفوف بأعمدة ثابتة (Option، Central site، Signal on fiber، Remote unit). أول كتلة في الـRemote مظللة (O/E). يُذكر أن الـUplink محذوف للوضوح |
| 7 | جدول + Line chart | جدول تعريف المقارنة (Systems، Endpoints، Signal، Medium، Criterion، Assumptions). Line chart أصلي من 0 إلى 400 m: Coax باللون الأسود، وRFoF بـLc=20 dB باللون Navy، وبـLc=40 dB باللون Navy الفاتح. محاور معنونة بالوحدات. صندوق نتيجة يذكر صيغة طول التعادل L* |
| 8 | جدول المقارنة | سطر تعريف المقارنة فوق الجدول. 7 معايير × نظامان. يتضمن رقم CPRI المحسوب مع ذكر أنه محسوب |
| 9 | جدول الفوائد | ثلاثة أعمدة (Benefit \| Holds when \| Does not imply) |
| 10 | SFDR | رسم تخطيطي بلا قيم، ويُكتب ذلك صراحة. Fundamental بميل 1، وIMD3 بميل 3، وNoise floor متقطع، وسهم SFDR بينهما |
| 11 | Case | BS hotel → Optical master units → 3 وحدات Fiber-fed. لوحتان: Reported وNot reported. صندوق "What the case supports" |
| 12 | جدول الاستنتاجات | عمود Evidence يحيل إلى رقم الشريحة |
| A3 | RAU types | DL وUL منفصلان. أسهم الـUplink تتجه نحو الـFiber |
| A4 | Line chart | Data labels بخانة عشرية واحدة. العنوان "Higher value = lower BER" |
| A5 | 5G/6G demo | فرعان من الـOptical coupler. Laser λ2 يدخل الـCoupler الثاني. UTC-PD يولّد f_THz |

**الصور:** حُذفت الصور النقطية الخمس كلها (منخفضة الدقة أو ملتقطة كلقطات شاشة) وأعيد رسمها كأشكال Vector أصلية داخل PowerPoint. تبقى واضحة عند أي تكبير، وكل كتلة وتسمية فيها قابلة للتحرير.

---

## G. الـAppendix المقترح (منفّذ في الملف)

| رقم | المحتوى | سبب النقل إلى الـAppendix |
|---|---|---|
| A1 | Glossary (18 مصطلحًا) | مرجعي، ويغني عن شريحة المصطلحات الأصلية |
| A2 | جدول الفقد عند 100 m و1 km و10 km، مصحح ويتضمن Lc | تفصيل رقمي يدعم الشريحة 7 |
| A3 | أنواع الـRAU (BBoF وIFoF وRFoF)، معاد رسمها | تفصيل يتجاوز حاجة الحجة الرئيسية |
| A4 | BER مقابل CSR | نتيجة تجريبية لوصلة واحدة |
| A5 | عرض 5G + 6G | عرض بحثي، لا نشر تجاري |
| A6 | حساب معدل CPRI ونتائج Li et al. | للأسئلة الكمية |
| A7 | خريطة المعايير والمواصفات | للأسئلة عن المعايير |
| A8 | المراجع | — |

---

## H. أسئلة تقنية متوقعة وإجابات محددة الحدود

**1. لماذا لا نقارن مباشرة 0.2 dB/km بـ22 dB/100 m؟**
لأن المقارنة الصحيحة بين وصلتين كاملتين من منفذ RF إلى منفذ RF. وصلة RoF تحمل فقد تحويل ثابتًا Lc لا يعتمد على الطول. لذلك يوجد طول تعادل L* = Lc / (0.222 − 0.0005) dB/m. يبلغ نحو 90 m عند Lc = 20 dB، ونحو 180 m عند Lc = 40 dB.
- **الحدود:** قيمة Lc افتراض يجب استبداله بقيمة الـDatasheet.
- **المصادر:** LMR-400 datasheet؛ Cox (2004).

**2. لماذا 1 dB ضوئي يعني 2 dB في الـRF؟**
في IM/DD يتناسب تيار الـPhotodiode مع القدرة الضوئية، وقدرة الـRF مع مربع التيار.
- **الحدود:** لا ينطبق على الكشف المتماسك (Coherent detection).
- **المصدر:** Cox (2004).

**3. هل يزيد RoF سعة الشبكة اللاسلكية؟**
لا. هو ينقل إشارة موجودة. سعة المستخدم يحددها الطيف والـSINR وعدد طبقات MIMO وكثافة الخلايا. قد يتيح RoF تكثيف نقاط الهوائي، لكن الزيادة تأتي من التكثيف لا من الألياف.

**4. ما الفرق بين A-RoF وCPRI من حيث سعة النقل؟**
CPRI: R = fs × 2 × N × 16/15 × line code. لحالة LTE 20 MHz (15-bit) الناتج 1228.8 Mb/s، وهو CPRI option 2. لحالة 100 MHz مع 64 هوائيًا الناتج ≈ 252 Gb/s قبل الـLine coding (محسوب). في A-RoF يشغل كل تيار هوائي تقريبًا عرض قناته الراديوية.
- **الحدود:** eCPRI (Split 7.2x) يخفض المعدل، ويتناسب مع عدد الطبقات والحمل.
- **المصدر:** CPRI V7.0.

**5. لماذا لا يُستخدم A-RoF في كل Fronthaul لـ5G إذا كان أقل استهلاكًا للسعة؟**
للأسباب التالية:
- الضوضاء والتشوه يتراكمان على طول الوصلة.
- لا توجد مراقبة على مستوى البت.
- الواجهات خاصة بكل مورد.
- منظومة O-RAN وeCPRI رقمية.

Li et al. (2021) يبلّغون في سيناريو نمذجة أن EVM لـA-RoF يتجاوز حد 3.5% لـ256-QAM.
- **الحدود:** لم يُتحقق من رقم 8% من النص الكامل (Verification required). حد 3.5% مأخوذ من 3GPP TS 38.104.

**6. ما أثر الـChromatic dispersion على وصلة RoF؟**
مع Double-sideband intensity modulation يتعرض الحزامان الجانبيان لإزاحات طور مختلفة. ينتج عن ذلك خبو في قدرة الـRF عند تراكيب معينة من التردد والطول. سبل التخفيف: العمل عند 1310 nm، أو SSB، أو IFoF.
- **الحدود:** الأثر صغير عند sub-6 GHz لمسافات المباني القصيرة. لا أقدّم رقمًا دون حساب لحالة محددة.
- **المصدر:** Gliese et al. (1996).

**7. هل وحدة الـRAU خالية من التعقيد أو لا تحتاج تغذية؟**
لا. تحتوي على Laser وPhotodiode ومكبرات وDuplexer ومصدر تغذية. هي أبسط من الـRRH لأنها بلا DAC/ADC وبلا معالجة Baseband.

**8. هل WDM ضروري؟**
لا. الوصلة النقطية بليفين وصلة RoF كاملة. يُستخدم WDM لتقليل عدد الألياف عند مشاركة كابل واحد.

**9. ما الذي تثبته حالة Maracanã وMineirão؟**
تثبت جدوى DAS ليفي متعدد المشغلين (5 مشغلين، 2G/3G/4G). لا تقدّم Link budget ولا قياسات سعة ولا مقارنة تكلفة. ولا تحدد ما إذا كانت كل الأنظمة الفرعية تنقل RF تماثليًا أو Fronthaul رقميًا.
- **المصادر:** Axell PR (06/2014)؛ RFS PR (10/06/2014).

**10. هل RoF أقل تكلفة؟**
لا يمكن الإجابة عمومًا. التكلفة تعتمد على توفر الألياف، وطول المسارات، وعدد النطاقات، وتكلفة المعدات. يحتاج ذلك إلى BoM لموقع محدد. لا يقدّم العرض ادعاء تكلفة.

**11. ما زمن التأخير الذي تضيفه الوصلة؟**
زمن الانتشار في الألياف ≈ 4.9 µs/km (Group index ≈ 1.47). لا يضيف A-RoF زمن Sampling أو Framing. التأخير الكلي في الـRAN تهيمن عليه معالجة الـBaseband.

**12. ما المعايير الحاكمة؟**
- ITU-T G.9803 (2018) وتعديلاته: متطلبات أنظمة RoF.
- G.Suppl.55 (10/2025): تقنيات RoF وتطبيقاتها.
- CPRI وeCPRI: مواصفات صناعية للـFronthaul الرقمي.
- **تحفظ:** مضمون Amd. 2 من G.9803 منقول عن العرض الأصلي ويحتاج مطابقة مع النص.

---

## الملحق: Slide text and notes (مستخرج آليًا من الملف)

```text
<!-- Slide number: 1 -->
Radio over Fiber (RoF)
Transport of radio waveforms over optical fiber: signal path, architectures, alternatives and limits
Technical review · 15 minutes · two speakers
Speaker A: problem, definition, signal path, architectures, RoF types
Speaker B: comparisons, benefits and conditions, limitations, case, conclusions
UE
Optical fiber: analog radio waveform
Central radio equipment
E/O
O/E
Remote antenna unit

### Notes:
Timing: 0:20 (Speaker A).
Purpose: state the subject and the division of work between the two speakers.
The strip at the bottom is the scope of the talk in one line: the optical segment between the central radio equipment and the remote antenna unit. Everything that follows is about that segment, its alternatives, and the conditions under which it is the right choice.

<!-- Slide number: 2 -->
Problem and scope
Engineering problem
Scope of this talk
Tunnels, stadiums and large buildings cannot be covered from one antenna site; radio power must be distributed over many antenna points.
Radio equipment is often centralized (equipment room or base-station hotel) to share power, cooling, maintenance and multi-operator access.
Question: how to carry the radio signal between the central equipment and each antenna point, over tens of metres to several kilometres, within a loss, noise, distortion and latency budget.
In scope: the transport segment between central equipment and remote antenna units (fronthaul or DAS feeder), downlink and uplink.
Out of scope: backhaul to the core network, air-interface design, spectrum and radio planning.
Alternatives compared: passive coaxial feeder; digital fronthaul (CPRI / eCPRI).
Transport segment: subject of this talk
UE
Core network
Central radio equipment (base station / BBU)
Remote antenna points (× N)
Backhaul
RF, IF or digital samples
Air interface
digital, packet
depends on transport option
Electrical (RF / IF / digital)
Wireless (over the air)
Downlink direction shown; uplink is the reverse path.
2

### Notes:
Timing: 1:15 (Speaker A).
Logic: start from the engineering need, not from the technology. The need is to distribute one radio signal to many antenna points that are physically far from the radio equipment. Centralization is a design choice with its own reasons (shared power, cooling, maintenance, multi-operator hosting); it is what creates the transport problem.
Point out explicitly that backhaul is out of scope: RoF is not a backhaul technology, and confusing the two is a common error in the source material.
The three alternatives named here are the only ones compared later; microwave point-to-point links are excluded because they serve backhaul, not an antenna feeder.

<!-- Slide number: 3 -->
Definition: what RoF transports, and what it does not
Radio over Fiber (RoF): an optical link that carries an analog radio waveform, at RF or IF, using electrical-to-optical (E/O) conversion at one end and optical-to-electrical (O/E) conversion at the other. The radio signal is generated and demodulated outside the link.

| Term | Meaning used in this talk |
| --- | --- |
| RF | Waveform at the air-interface carrier frequency; radiated after amplification and filtering. |
| IF | Same modulation on a lower carrier; the remote unit needs a mixer and local oscillator (LO) to reach RF. |
| Baseband (I/Q) | Complex envelope centred at 0 Hz; reaching RF needs a DAC and up-conversion. Digital fronthaul carries it as samples. |
| Fronthaul / backhaul | Fronthaul: central baseband or radio site ↔ remote radio or antenna unit. Backhaul: base station ↔ core network. |
| Transport vs wireless capacity | Transport: what the link carries (bit rate, or analog bandwidth and dynamic range). Wireless: user throughput, set by spectrum, SINR, MIMO layers and cell density. |
| Analog RoF vs digital fronthaul | Analog waveform on fiber, versus serialized digital samples (CPRI) or packets (eCPRI). Some literature calls the latter "digital RoF". |

RoF moves the point where the radio signal is radiated. It does not add spectrum or air-interface capacity.
Sources: ITU-T G.Suppl.55 (10/2025), Radio-over-fibre technologies and their applications; ITU-T G.9803 (2018), Radio over fibre systems; CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).
3

### Notes:
Timing: 1:15 (Speaker A).
Logic: fix the vocabulary before any claim is made. Every later comparison depends on these distinctions.
Emphasize the boundary: in this talk 'RoF' means an analog waveform on the fiber. Digitized I/Q transport (CPRI) is called digital fronthaul. ITU-T G.Suppl.55 also describes digitized variants, and some papers call CPRI-type links 'digital RoF'; we keep the terms separate to avoid attributing analog properties to digital links and vice versa.
The last line answers a frequent misconception: fiber capacity does not translate into wireless capacity. Users receive what the air interface delivers.

<!-- Slide number: 4 -->
End-to-end signal path: downlink and uplink
Central site
Single-mode fiber, length L
Remote antenna unit (RAU)
Downlink
RF over the air to / from UE
Base-station RF port (DL out)
E/O: laser (direct) or laser + MZM
O/E: photodiode
Amp + BPF
PA
Duplexer
intensity-modulated, λ1
Base-station RF port (UL in)
O/E: photodiode + RF amp
E/O: laser diode
LNA
λ2 or second fiber
Uplink
Conversion points
DL: E/O at central site, O/E at RAU. UL: E/O at RAU, O/E at central site. Each conversion adds noise and distortion.
Optical loss vs RF loss
Intensity modulation with direct detection: RF power ∝ (optical power)². 1 dB optical loss → 2 dB RF loss.
Multiplexing
DL and UL use separate fibers or wavelengths. WDM is optional; needed only when several links share one fiber.
Electrical (RF / IF / digital)
Optical (fiber)
Wireless (over the air)
Sources: C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge Univ. Press, 2004; ITU-T G.Suppl.55 (10/2025). MZM: Mach-Zehnder modulator; BPF: band-pass filter; PA: power amplifier; LNA: low-noise amplifier.
4

### Notes:
Timing: 1:45 (Speaker A).
Walk the downlink left to right, then the uplink right to left. Stop at each conversion point.
Four optoelectronic conversions exist in a bidirectional link: two at each end. Each adds noise and distortion; this is why RoF link performance is not the same as fiber attenuation.
Square-law detection: the photodiode current is proportional to optical power, and RF power is proportional to current squared. Therefore 1 dB of optical loss costs 2 dB of RF power (Cox, 2004). This is the correct way to translate fiber loss into the RF budget.
WDM is drawn as optional on purpose: a point-to-point link with two fibers is a complete RoF link. WDM only reduces fiber count when several links share a cable.
Downlink and uplink have different requirements: downlink is limited mainly by distortion at high drive levels; uplink by the link noise figure, because received signals are weak.

<!-- Slide number: 5 -->
Architecture: where the RoF link sits in the network
Fronthaul: head-end ↔ RAU. This is the RoF link.
Backhaul: base station ↔ core; digital, packet. Not RoF.
Topology: star; one fiber pair or wavelength pair per RAU. WDM or cascaded RAUs reduce fiber count.
RAU contents: O/E, E/O, RF amplifiers, filters, duplexer, power supply, alarms.
C-RAN variant: BBU pool and RRHs; the link carries digital fronthaul instead.
RAU 1
Base-station hotel
Head-end: RF combining, E/O (DL), O/E (UL)
Operator A radio
Core network
RAU 2
Backhaul
Operator B radio
Operator C radio
RF (coax)
RAU n
Fiber links: analog RF, downlink and uplink
Electrical (RF / IF / digital)
Optical (fiber)
Wireless (over the air)
Generic multi-operator fiber DAS / centralized radio architecture. Sources: ITU-T G.Suppl.55 (10/2025); ITU-T G.9803 (2018).
5

### Notes:
Timing: 1:30 (Speaker A).
Logic: place the link in a real deployment so the audience can separate fronthaul from backhaul.
Backhaul is digital and packet-based; it is not affected by the choice of RoF. The RoF link is only the head-end-to-RAU segment.
The head-end combines RF from several operators and bands before E/O conversion. This is what makes the analog link format-transparent, within its bandwidth and dynamic range.
State the topology honestly: a star of point-to-point links. Fiber count can be reduced by WDM or by cascading remote units, but each option has its own cost and limits.
Do not describe the RAU as passive: it contains lasers, photodiodes, amplifiers and a power supply.
Same placement applies to centralized RAN (C-RAN): replace the head-end with a BBU pool and the RAU with an RRH; the link then carries digital fronthaul, not analog RoF.

<!-- Slide number: 6 -->
RoF types: what is on the fiber sets what the remote unit contains
Option
Central site
Signal on fiber
Remote unit: downlink functions
RFoF
analog RF
Radio: DAC + up-conversion to RF
E/O
O/E
Amp + BPF
PA
Analog RF waveform
IFoF
analog IF
Radio: DAC + up-conversion to IF
E/O
O/E
Mixer + LO
Amp + BPF
PA
Analog IF waveform
Digital fronthaul
CPRI; not analog RoF
BBU: PHY → I/Q samples
Framer + optical TRx
Optical TRx + deframer
DAC
Up-conv. + LO
PA
Serial digital I/Q samples
Remote-unit complexity increases from RFoF to digital fronthaul (frequency conversion, then DAC/ADC and framing).
Fiber transport requirement increases in the opposite direction: digitized samples need far more capacity than the analog waveform (slide 8).
Electrical (RF / IF / digital)
Optical (fiber)
Uplink chains (LNA, E/O at remote; O/E at central) omitted for clarity.
6

### Notes:
Timing: 1:30 (Speaker A). Handover to Speaker B after this slide (target elapsed time ≈ 7:15).
Logic: the functional split decides two opposite quantities: remote-unit complexity and fiber transport requirement.
RFoF: simplest remote downlink chain, but the optoelectronics must operate at the carrier frequency, which becomes difficult and costly at mmWave; dispersion effects also grow with RF frequency.
IFoF: optoelectronics run at a lower frequency; the price is a mixer and a stable LO at every RAU.
Digital fronthaul: robust to fiber impairments because it is digital, but the remote unit is a full radio (RRH) and the bit rate is high. This row is not RoF in the strict sense; it is shown because it is the main alternative.
Analog baseband-over-fiber also appears in research literature (e.g. Electronics 9(11), 1785, 2020); it is listed in the appendix, not used in the main argument.

<!-- Slide number: 7 -->
Comparison 1: passive coaxial feeder vs analog RFoF link

### Chart: RF-to-RF loss vs length at 2.5 GHz (downlink, unamplified)

| Category | Coax, LMR-400 class | RFoF, Lc = 20 dB (assumed) | RFoF, Lc = 40 dB (assumed) |
| --- | --- | --- | --- |
| 0 | 0.0 | 20.0 | 40.0 |
| 50 | 11.1 | 20.0 | 40.0 |
| 100 | 22.2 | 20.1 | 40.1 |
| 150 | 33.3 | 20.1 | 40.1 |
| 200 | 44.4 | 20.1 | 40.1 |
| 250 | 55.5 | 20.1 | 40.1 |
| 300 | 66.6 | 20.2 | 40.2 |
| 350 | 77.7 | 20.2 | 40.2 |
| 400 | 88.8 | 20.2 | 40.2 |

| Item | Definition |
| --- | --- |
| Systems | (1) Passive coax, LMR-400 class, 50 Ω. (2) Analog RFoF link, no RF amplifiers. |
| Endpoints | Head-end RF output port → remote antenna port (downlink) |
| Signal | RF passband at 2.5 GHz |
| Medium | Coax; G.652.D single-mode fiber at 1550 nm |
| Criterion | RF-to-RF insertion loss versus length |
| Assumptions | Coax 22.2 dB/100 m. Fiber 0.25 dB/km optical = 0.5 dB/km RF. RoF conversion loss Lc = 20–40 dB (assumed). |

Result under these assumptions: break-even length L* = Lc / (0.222 − 0.0005 dB/m) ≈ 90 m (Lc = 20 dB) to 180 m (Lc = 40 dB). Below L*, passive coax has lower RF loss; above L*, RFoF does. Practical fiber DAS equipment adds RF gain at both ends, so the deciding metrics become noise figure, dynamic range and power consumption, not loss alone.
Coax: Times Microwave LMR-400 datasheet, 22.2 dB/100 m at 2500 MHz. Fiber: G.652.D cable datasheets, ≤ 0.22–0.25 dB/km at 1550 nm. Lc range is an assumption: verify against the datasheet of the equipment under evaluation.
7

### Notes:
Timing: 1:45 (Speaker B).
Logic: replace the original 'fiber loses 0.2 dB/km, coax loses 22 dB/100 m' argument, which compared a cable with a cable and ignored the conversion loss of the RoF link.
Model: coax loss = 0.222 dB/m × L. RoF RF loss = Lc + 2 × 0.25 dB/km × L. The factor 2 is square-law detection.
Lc (RF-to-RF conversion loss of an unamplified link) is device-specific. The 20–40 dB range is an assumption for illustration and must be replaced with the datasheet value of the equipment under evaluation. Cox (2004) treats link gain in detail; do not quote a single number without the device parameters.
Break-even L* = Lc / (0.222 − 0.0005) ≈ 90 m for 20 dB and ≈ 180 m for 40 dB.
Key message: loss alone does not decide. Commercial fiber DAS units include RF gain at both ends, so the decisive metrics are noise figure (uplink), dynamic range (multi-carrier downlink) and power consumption.

<!-- Slide number: 8 -->
Comparison 2: analog RoF vs digital fronthaul (CPRI)
Systems: analog RFoF / IFoF vs CPRI-type digital fronthaul · Endpoints: central site ↔ remote unit · Medium: single-mode fiber · Assumption: same radio carrier and antenna count

| Criterion | Analog RoF (RFoF / IFoF) | Digital fronthaul (CPRI) |
| --- | --- | --- |
| Signal on fiber | Analog RF or IF waveform | Serialized time-domain I/Q samples (CPRI); packets (eCPRI) |
| Transport requirement | Analog bandwidth ≈ radio channel bandwidth per antenna stream, plus required dynamic range | Bit rate = sample rate × 2 × bits per sample × overheads. 20 MHz LTE, 1 antenna: 1228.8 Mb/s (CPRI option 2) |
| Scaling | One RF / IF channel (subcarrier or wavelength) per antenna stream | Linear in antenna count and sample rate. 100 MHz, 64 antennas ≈ 252 Gb/s before line coding (computed) |
| Remote unit | O/E, E/O, amplifiers, filters (+ mixer and LO for IFoF) | DAC / ADC, framing, up / down-conversion, LO, amplifiers (RRH) |
| Dominant impairments | Noise, nonlinear distortion, dispersion-induced RF power fading; accumulate along the link | Quantization noise, fixed by bit width; independent of length while bit errors are negligible |
| Monitoring and interoperability | No native bit-level monitoring; largely vendor-specific. ITU-T G.9803 sets system requirements | Bit-level monitoring; CPRI / eCPRI specifications; O-RAN split 7.2x for multi-vendor |
| Added latency | Fiber propagation ≈ 5 µs/km; no sampling or framing | Fiber propagation ≈ 5 µs/km + framing and buffering (implementation-specific) |

Sources: CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019); ITU-T G.9803 (2018) and Amd. 2 (2022); Y. Li et al., arXiv:2111.13851 (2021). Propagation delay from group index ≈ 1.47. eCPRI split 7.2x rate scales with MIMO layers and load, not antenna count.
8

### Notes:
Timing: 1:30 (Speaker B).
Logic: this is the comparison that matters for mobile networks, because digital fronthaul is the incumbent for C-RAN.
CPRI rate, worked: 20 MHz LTE uses 30.72 Msample/s. 30.72 × 2 (I and Q) × 15 bits × 16/15 (control words) × 10/8 (8B/10B line code) = 1228.8 Mb/s, which is CPRI line-rate option 2.
Scaling example (computed with the same formula, no compression, before line coding): 100 MHz NR at 122.88 Msample/s gives 3.93 Gb/s per antenna; 64 antennas give about 252 Gb/s. This scaling is the argument for analog transport or for eCPRI splits.
Fairness: digital fronthaul quality is set by quantization and is independent of fiber length until bit errors appear; analog quality degrades along the link. Analog links also lack bit-level monitoring.
Li et al. (2021) report a modeled case in which A-RoF needs much less fiber bandwidth but exceeds the 3GPP EVM limit for 256-QAM; see appendix A6. Those figures are scenario-specific.

<!-- Slide number: 9 -->
Benefits, and the conditions under which they hold

| Benefit | Holds when | Does not imply |
| --- | --- | --- |
| Low fiber attenuation (≈ 0.2–0.25 dB/km cabled SMF at 1550 nm) | Link is longer than the break-even length set by conversion loss (slide 7) | Low RF-to-RF loss for short links; conversion loss is fixed |
| Fiber span immune to electromagnetic pickup; galvanic isolation | Dielectric cable is used | Immunity of RAU electronics or of the air interface |
| Centralized radio equipment (base-station hotel, multi-operator) | RFoF or IFoF; head-end hosts all baseband and radio processing | No remote power or maintenance: RAU has lasers, amplifiers, power supply |
| Format transparency: multi-band, multi-operator, multi-technology on one link | Within optoelectronic bandwidth, linearity and dynamic range | Any number of bands: all carriers share one link's dynamic range |
| Small, light cable | Compared with coax of similar loss over the same route | Lower total installed cost: site-specific, not established here |
| Low added transport latency (≈ 5 µs/km, no sampling or framing) | Analog link | Lower end-to-end RAN latency, which baseband processing dominates |

Sources: G.652.D cable datasheets (attenuation); ITU-T G.Suppl.55 (10/2025); C. H. Cox III, Analog Optical Links, 2004.
9

### Notes:
Timing: 1:00 (Speaker B).
Logic: each benefit is stated with its condition and with what it does not imply. This directly corrects the original slides, which attributed fiber properties to the whole RoF system.
Row 1 connects to slide 7: low fiber attenuation helps only once the link is longer than the break-even length.
Row 3: centralization is real, but the RAU still has active optoelectronics and needs power. 'Simple RAU' is true only relative to an RRH, and only for RFoF.
Row 4: transparency is the main practical reason fiber DAS is used for multi-operator venues. All carriers share one link's dynamic range, so adding carriers reduces per-carrier headroom.
Row 5: cost is site-specific. No general cost claim is made; it requires a bill of materials for a given site.

<!-- Slide number: 10 -->
Limitations and engineering trade-offs
Noise and dynamic range: laser RIN, shot noise and receiver thermal noise set a noise floor; the link noise figure limits uplink sensitivity and the number of carriers per link.
Nonlinear distortion: laser and modulator nonlinearity creates intermodulation; higher drive improves SNR until distortion dominates (SFDR).
Chromatic dispersion: with double-sideband intensity modulation, RF power fades at frequency- and length-dependent nulls. Mitigation: 1310 nm, single-sideband modulation, IFoF.
Fiber and topology: one fiber pair or wavelength pair per RAU; new fiber needs civil works and permits.
Remote power: RAU lasers and amplifiers need local power or hybrid fiber–copper cable.
Operations: no bit-level performance monitoring on the analog link; interfaces largely vendor-specific.
Noise vs distortion: SFDR (illustrative, no values)
RF output (dB)
Fundamental (slope 1)
SFDR
IMD3 (slope 3)
Noise floor
RF input power (dB)
Sources: C. H. Cox III, Analog Optical Links, 2004; U. Gliese et al., IEEE Trans. Microwave Theory Tech. 44(10), 1996 (dispersion-induced RF power fading); D. Wake et al., J. Lightwave Technol. 28(16), 2010.
10

### Notes:
Timing: 1:15 (Speaker B).
Logic: the limitations are physical mechanisms, not general disadvantages.
Noise vs distortion is the central analog trade-off. The figure is the standard spurious-free dynamic range construction: the fundamental rises 1 dB per dB of input, third-order intermodulation rises 3 dB per dB. SFDR is the input range between the noise floor and the point where IMD3 reaches the noise floor. It is illustrative and has no values.
Dispersion: with double-sideband intensity modulation, the two optical sidebands experience different phase shifts in a dispersive fiber; after detection they interfere and the RF power fades at specific frequency-length combinations (Gliese et al., 1996). This is a design constraint at mmWave on 1550 nm, not a reason to avoid RoF at sub-6 GHz over short indoor runs.
Remote power is often underestimated in venue projects; hybrid fiber-copper cables are one documented solution (slide 11).

<!-- Slide number: 11 -->
Documented case: Maracanã and Mineirão stadiums (2014)
Reported
Fiber-fed remote unit
Optical DAS for five mobile operators, 2G / 3G / 4G; combined stadium capacity over 141,000 (Axell Wireless, June 2014).
Maracanã: hybrid fiber + DC power cable feeding remote radio units; 2G, 3G, 4G and iDEN (RFS, 10 June 2014).
Base-station hotel: 5 operators, 2G / 3G / 4G
Optical master units: RF ↔ optical
Fiber-fed remote unit
RF
Fiber-fed remote unit
Fiber (hybrid fiber + DC power cable at Maracanã)
Not reported
Stands, concourses, public areas
Link budgets, noise figure, measured capacity, cost against alternatives.
Transport format per subsystem (analog RF or digital).
Electrical (RF / IF / digital)
Optical (fiber)
What the case supports: feasibility of a multi-operator, multi-technology fiber-fed DAS in large venues. It does not support quantitative performance or cost claims.
Sources: Axell Wireless press release, June 2014 (prnewswire.co.uk); RFS press release, 10 June 2014 (globenewswire.com); PBE Axell case study "Brazilian Sports Stadiums" (equipment names: verification required).
11

### Notes:
Timing: 1:00 (Speaker B).
Logic: one documented deployment, with a clear statement of what the sources do and do not show.
Facts as reported by the vendors: Axell Wireless (June 2014) supplied optical DAS for venues including Maracanã and Mineirão, combined capacity over 141,000, five operators, 2G/3G/4G. RFS (10 June 2014) reported its HYBRIFLEX hybrid fiber and DC power cable at Maracanã, feeding remote radio units, for 2G, 3G, 4G and iDEN.
The PBE Axell case study cited in the original deck names Optical Master Units converting RF to optical; that page could not be retrieved during this review, so treat equipment model names as requiring verification.
Do not claim performance from this case. The sources are vendor press releases; they contain no link budgets, noise figures or capacity measurements. They also do not state whether every subsystem used analog RF transport or digital fronthaul to the remote radios.

<!-- Slide number: 12 -->
Conclusions

| # | Conclusion | Evidence |
| --- | --- | --- |
| 1 | RoF transports an existing radio signal. It does not add spectrum or air-interface capacity. | Slide 3 |
| 2 | Against passive coax at 2.5 GHz, unamplified RFoF has lower RF loss only beyond a break-even length set by conversion loss (≈ 90–180 m under the stated assumptions). | Slide 7 |
| 3 | Against digital fronthaul, analog RoF needs far less fiber capacity and no DAC/ADC at the remote unit, at the cost of noise, distortion, dispersion and weaker monitoring. | Slides 8, 10 |
| 4 | Documented deployments include multi-operator fiber-fed DAS in large venues; vendor sources support feasibility, not performance. | Slide 11 |
| 5 | Selection criteria: fiber availability, link length, number of bands and operators, required noise figure and dynamic range, remote power, monitoring needs. | Slides 7–10 |

12

### Notes:
Timing: 1:00 (Speaker B). Then open questions.
Logic: each conclusion is traceable to a slide. If challenged, go back to that slide.
Avoid generalizing beyond the evidence: the break-even length depends on the assumed conversion loss; the deployment case is evidence of feasibility only.
The final row is a decision checklist, not a recommendation: whether RoF is appropriate depends on the site.

<!-- Slide number: 13 -->
Questions
Reference material in the appendix:
A1 Glossary
A2 Loss figures at 100 m, 1 km and 10 km
A3 Remote antenna unit types (BBoF, IFoF, RFoF)
A4 Measured BER versus carrier-to-sideband ratio
A5 Research demonstration: 5G-NR and a candidate 6G signal on one fiber
A6 Fronthaul bit-rate calculation and reported analog vs digital comparison
A7 Standards and specifications
A8 References
13

### Notes:
Use appendix slides A1–A8 for detailed answers. Expected questions and bounded answers are in the review report, section H.

<!-- Slide number: 14 -->
A1 Glossary

| Term | Meaning |
| --- | --- |
| BBU | Baseband unit: PHY / MAC processing at the central site |
| RRH / RRU | Remote radio head / unit: DAC/ADC, frequency conversion, PA/LNA; fed by digital fronthaul |
| RAU | Remote antenna unit of an analog RoF link: O/E, E/O, RF amplifiers, filters |
| DAS | Distributed antenna system: one signal source, many antenna points |
| WDM | Wavelength-division multiplexing: several wavelengths on one fiber |
| MZM | Mach-Zehnder modulator: external intensity modulator |
| IM/DD | Intensity modulation, direct detection |
| LO | Local oscillator, used for frequency conversion |
| SMF | Single-mode fiber (ITU-T G.652 family) |

| Term | Meaning |
| --- | --- |
| TIA / PA / LNA | Transimpedance / power / low-noise amplifier |
| RIN | Relative intensity noise of the laser |
| SFDR | Spurious-free dynamic range |
| CSR | Optical carrier-to-sideband power ratio |
| BER | Bit error ratio |
| EVM | Error vector magnitude; 3GPP limit for 256-QAM: 3.5 % |
| CPRI | Common Public Radio Interface: serial digital I/Q fronthaul |
| eCPRI | Packet-based fronthaul; supports intra-PHY splits |
| C-RAN | Centralized RAN: baseband pooled at a central site |

EVM limit: 3GPP TS 38.104, base-station transmitter EVM requirements.
14

### Notes:
Reference only.

<!-- Slide number: 15 -->
A2 Loss figures at 100 m, 1 km and 10 km (2.5 GHz)

| Length | Coax, LMR-400 class (22.2 dB/100 m) | Fiber, optical loss (0.25 dB/km) | RFoF, RF loss = Lc + 2 × optical loss |
| --- | --- | --- | --- |
| 100 m | 22.2 dB | 0.025 dB | Lc + 0.05 dB |
| 1 km | 222 dB (extrapolated; not built passively) | 0.25 dB | Lc + 0.5 dB |
| 10 km | 2,220 dB (extrapolated; not built passively) | 2.5 dB | Lc + 5 dB |

Lc: fixed RF-to-RF conversion loss of the unamplified RoF link; device-specific. Verification required against equipment datasheets.
Optical-to-RF factor of 2 applies to intensity modulation with direct detection (square-law photodetection).
Splice and connector losses are excluded from both columns.
Sources: Times Microwave LMR-400 datasheet; G.652.D cable datasheets; C. H. Cox III, Analog Optical Links, 2004.
15

### Notes:
Corrects the original table, which compared cable loss only and omitted the RoF conversion loss Lc.
The coax values at 1 km and 10 km are linear extrapolations; such runs are not built with passive coax. Coax systems over such distances (e.g. HFC cable TV) use in-line amplifiers, so 'no amplifier could recover it' is not a valid statement; the valid statement is that a passive coax feeder is impractical at these lengths.

<!-- Slide number: 16 -->
A3 Remote antenna unit types: BBoF, IFoF, RFoF
Downlink: fiber → antenna
Uplink: antenna → fiber
BBoF
On fiber: Baseband
PD
TIA
MOD
Mixer + LO
PA
LD
DEMOD
Mixer + LO
LNA
IFoF
On fiber: IF
PD
TIA
Mixer + LO
PA
LD
Mixer + LO
LNA
RFoF
On fiber: RF
PD
TIA
PA
LD
LNA
PD: photodiode · TIA: transimpedance amplifier · MOD / DEMOD: modulator / demodulator · LO: local oscillator · PA: power amplifier · LNA: low-noise amplifier · LD: laser diode. Shaded blocks are O/E (downlink) and E/O (uplink).
Redrawn from: "Radio over Fiber: An Alternative Broadband Network Technology for IoT," Electronics 9(11), 1785 (2020), Fig. 3. DOI: 10.3390/electronics9111785.
16

### Notes:
Redrawn from Electronics 9(11), 1785 (2020), Fig. 3, with downlink and uplink chains separated.
In this figure, BBoF denotes analog baseband over fiber: the RAU needs a modulator, mixer and LO. This differs from digital fronthaul, which carries sampled baseband.
RFoF has no frequency conversion at the RAU but still contains a photodiode, TIA, PA, LNA and a laser diode, plus power supply.

<!-- Slide number: 17 -->
A4 Measured BER versus carrier-to-sideband ratio (one experimental link)

### Chart: Higher value = lower BER

| Category | −log10(BER) |
| --- | --- |
| 0 | 2.0 |
| 5 | 3.0 |
| 10 | 3.5 |
| 15 | 3.5 |
| 20 | 4.3 |
| 25 | 4.4 |
| 30 | 3.3 |

Setup: 10 km SMF plus 3 m wireless link (as reported).
Trend: BER improves up to CSR ≈ 25 dB, then degrades at 30 dB.
Mechanism: distortion dominates at low CSR; noise dominates at high CSR.
Limit: result applies to the tested link only.
Status: values read from the published plot; verification required.
Redrawn from: M. U. Hadi and G. Murtaza, "Fibre Wireless Distributed Antenna Systems for 5G and 6G Services," Electronics 12(1), 64 (2023), Fig. 6. DOI: 10.3390/electronics12010064.
17

### Notes:
Values are approximate readings from the published plot, carried over from the original deck. They were not re-checked against the paper during this review: verification required.
Interpretation: at low CSR the optical sidebands are strong relative to the carrier and distortion dominates; at high CSR most optical power is in the unmodulated carrier and the detected signal is weak relative to noise. The optimum is specific to the tested link (10 km SMF plus 3 m wireless).
Note that −log10(BER) ≈ 2 corresponds to BER ≈ 1e-2, above common hard-decision FEC thresholds (≈ 3.8e-3).

<!-- Slide number: 18 -->
A5 Research demonstration: 5G-NR and a candidate 6G signal on one fiber
PIN photodiode (O/E)
LPF
5G RAU (antenna side)
5G-NR: 5 × 50 MHz at IF1 = 1.14 GHz
Tx (E/O)
Optical coupler
fiber
Candidate 6G at IF2 = 12 GHz
BPF (optical)
Optical coupler
UTC-PD (O/E)
6G RAU: THz output (f_THz)
Beat of λ1 sideband and λ2 → f_THz
Laser λ2
Electrical (RF / IF / digital)
Optical (fiber)
Research demonstration of simultaneous transport. No deployment, cost or capacity conclusion follows from it.
Redrawn and simplified from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 2. DOI: 10.3390/electronics12010064.
18

### Notes:
Laboratory demonstration, not a deployed system. '6G' is the authors' label for a candidate THz signal.
Mechanism of the 6G branch: the IF2 signal is carried on the optical sideband; a second laser at λ2 is combined, and a uni-travelling-carrier photodiode (UTC-PD) mixes the two optical tones so that the beat frequency falls in the THz range (photonic up-conversion).
Block names follow the published figure.

<!-- Slide number: 19 -->
A6 Fronthaul bit-rate calculation and reported analog vs digital comparison
CPRI-type rate per antenna-carrier
R = fs × 2 (I, Q) × N bits × 16/15 (control words) × line-code factor (10/8 for 8B/10B)

| Case | fs | N | Antennas | Result |
| --- | --- | --- | --- | --- |
| LTE 20 MHz | 30.72 Msample/s | 15 | 1 | 1228.8 Mb/s with 8B/10B (CPRI option 2) |
| NR 100 MHz | 122.88 Msample/s | 15 | 1 | 3.93 Gb/s before line coding |
| NR 100 MHz | 122.88 Msample/s | 15 | 64 | ≈ 252 Gb/s before line coding |

Reported modeled comparison (Li et al., 2021)
Up to 40× lower fiber bandwidth for analog RoF than digital RoF in one modeled case: 16 × 16 MIMO, 28 GHz carrier, 256-QAM.
In a modeled 256-QAM case, analog RoF EVM ≈ 8 % against the 3.5 % 3GPP limit; the digital case met the limit.
Both results are scenario-specific. Values carried over from the original deck: verification against the paper required.
Sources: CPRI Specification V7.0 (2015); 3GPP TS 38.104; Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, "Analogue Radio Over Fiber for Next-Generation RAN: Challenges and Opportunities," arXiv:2111.13851 (2021).
19

### Notes:
The CPRI calculation uses the specification's sample rates and overheads; check figures before quoting a different configuration.
Li et al. figures were carried over from the original deck; the arXiv full text could not be retrieved during this review. Verify the 40× and 8 % values against the paper before presenting them.

<!-- Slide number: 20 -->
A7 Standards and specifications

| Document | Body | Scope relevant to this talk |
| --- | --- | --- |
| G.9803 (2018), Amd. 1 (2019), Amd. 2 (2022) | ITU-T | Radio over fibre systems: system requirements; Amd. 2 covers RoF architectures and requirements for IMT-2020 mobile fronthaul |
| G.Suppl.55 (10/2025) | ITU-T | Radio-over-fibre technologies and their applications; earlier editions 07/2015, 12/2021, 12/2023 |
| G.652 | ITU-T | Characteristics of standard single-mode optical fibre and cable |
| CPRI Specification V7.0 (2015) | CPRI industry consortium | Serial digital I/Q interface between baseband and radio equipment |
| eCPRI Specification V2.0 (2019) | CPRI industry consortium | Packet-based fronthaul with intra-PHY functional splits |
| O-RAN fronthaul (split 7.2x) | O-RAN Alliance | Multi-vendor control, user and synchronization plane specification |
| TS 38.104 | 3GPP | NR base-station RF requirements, including transmitter EVM limits |

Edition dates of G.Suppl.55 from the ITU-T recommendation page. Amendment content of G.9803 as cited in the original deck: verification against ITU-T text recommended.
20

### Notes:
Reference only. CPRI and eCPRI are industry specifications, not ITU-T standards.

<!-- Slide number: 21 -->
A8 References
C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge University Press, 2004.
U. Gliese, S. Nørskov, T. N. Nielsen, "Chromatic dispersion in fiber-optic microwave and millimeter-wave links," IEEE Trans. Microwave Theory Tech., 44(10), 1996.
D. Wake, A. Nkansah, N. J. Gomes, "Radio over fiber link design for next generation wireless systems," J. Lightwave Technol., 28(16), 2010.
ITU-T G.9803 (2018), Radio over fibre systems; Amendment 1 (2019); Amendment 2 (2022).
ITU-T G-series Supplement 55 (10/2025), Radio-over-fibre (RoF) technologies and their applications.
ITU-T G.652, Characteristics of a single-mode optical fibre and cable.
CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).
3GPP TS 38.104, NR; Base Station (BS) radio transmission and reception.
Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, "Analogue Radio Over Fiber for Next-Generation RAN: Challenges and Opportunities," arXiv:2111.13851, 2021.
"Radio over Fiber: An Alternative Broadband Network Technology for IoT," Electronics 9(11), 1785, 2020. DOI: 10.3390/electronics9111785.
M. U. Hadi, G. Murtaza, "Fibre Wireless Distributed Antenna Systems for 5G and 6G Services," Electronics 12(1), 64, 2023. DOI: 10.3390/electronics12010064.
Times Microwave Systems, LMR-400 coaxial cable datasheet.
Axell Wireless press release on Brazilian stadium coverage, June 2014; RFS press release on Maracanã, 10 June 2014; PBE Axell case study "Brazilian Sports Stadiums".
21

### Notes:
The SolFinder Research video used in the original deck is a secondary source; it is not cited for any technical claim in this revision.
```
