# مراجعة تقنية لعرض Radio over Fiber (RoF)

**الملف الأصلي:** `Radio_over_Fiber_Reviewed_Final_v4.pptx`، ويضم 31 شريحة و5 صور نقطية (Raster).
**المخرجات:**
- `RoF_Technical_Review.pptx`: العرض المعاد بناؤه (النسخة الثانية، المبسطة)، ويضم 14 شريحة رئيسية و4 شرائح Appendix. كل شريحة فيها رسم أو Plot واحد كبير وسطر واحد فقط، والتفاصيل في الـSpeaker Notes.
- `figures/`: كل الرسوم والـPlots بصيغة PNG عالية الدقة (220 dpi).
- `make_figures.py`: يولّد الرسوم. الـPlots محسوبة من المعادلات المذكورة في الـNotes.
- `build_rof_deck.js`: يولّد العرض من الرسوم.
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

| # | الشريحة | الرسم | المتحدث | الوقت | التراكمي |
|---|---|---|---|---|---|
| 1 | Radio over Fiber (RoF) | مخطط الوصلة الأساسي | A | 0:20 | 0:20 |
| 2 | The problem | مقطع مبنى بهوائيات في كل طابق | A | 1:00 | 1:20 |
| 3 | What RoF is | الوصلة مع الطيف الكهربائي والضوئي | A | 1:15 | 2:35 |
| 4 | Signal path | مسار DL/UL ومواضع E/O وO/E | A | 1:30 | 4:05 |
| 5 | Where it sits in the network | Head-end ونجمة ألياف إلى RAUs | A | 1:15 | 5:20 |
| 6 | Three ways to use the fiber | الإشارة على الليف وسلسلة الوحدة البعيدة | A | 1:30 | 6:50 |
| — | **تسليم إلى المتحدث B** | | | 0:10 | 7:00 |
| 7 | Coax or fiber? | Plot: الفقد مقابل الطول وطول التعادل | B | 1:45 | 8:45 |
| 8 | Analog RoF vs digital fronthaul | Plot: معدل CPRI مقابل عدد الهوائيات | B | 1:30 | 10:15 |
| 9 | Benefit: low fiber loss | Plot: التوهين مقابل طول الموجة | B | 1:00 | 11:15 |
| 10 | Limit 1: chromatic dispersion | Plot: خبو قدرة الـRF مقابل التردد | B | 1:00 | 12:15 |
| 11 | Limit 2: noise vs distortion | Plot: SFDR | B | 1:00 | 13:15 |
| 12 | Case: Maracanã and Mineirão | مخطط ملعب بالـRemote units | B | 1:00 | 14:15 |
| 13 | When to choose analog RoF | Decision flow | B | 0:45 | 15:00 |
| 14 | Questions | — | A+B | — | — |
| A1–A4 | Appendix | RAU types، BER vs CSR، 5G/6G demo، References | — | — | — |

---

## D وE. نص الشرائح وSpeaker Notes

النص الإنجليزي الكامل لكل شريحة وملاحظات المتحدث موجودان داخل ملف `RoF_Technical_Review.pptx`، كلٌّ في Notes الشريحة الخاصة بها. أُلحقت نسخة نصية مستخرجة آليًا منهما في نهاية هذا التقرير (الملحق: Slide text and notes)، لتكون مرجعًا واحدًا لا يتعارض مع الملف.

مبدأ الـNotes: كل ملاحظة تشرح منطق الشريحة وحدود ادعائها، وتعطي الحساب أو المصدر عند الحاجة. لا تكرر نص الشريحة.

---

## F. تعليمات التصميم (النسخة الثانية)

- **القاعدة:** كل شريحة فيها عنوان قصير، وسطر واحد هو الرسالة، ورسم أو Plot يشغل معظم المساحة، وسطر مصدر صغير. كل الشرح والأرقام التفصيلية في الـSpeaker Notes.
- **الخط:** Arial في الشرائح، وLiberation Sans (المطابق لـArial) في الرسوم. العنوان 30 pt عريض أسود، والرسالة 18 pt رمادي داكن.
- **الألوان:** أبيض وأسود فقط، مع لون واحد وظيفي: البرتقالي (D55E00 من لوحة Okabe-Ito المستخدمة في الأوراق العلمية) للمسار الضوئي ولكتل E/O وO/E. الأزرق (0072B2) يُستخدم فقط كسلسلة ثالثة في Plot التشتت. لا Navy ولا تعبئات ملونة ولا صناديق خلفية.
- **الرسوم التخطيطية:** صناديق بإطار أسود رفيع. كتل التحويل بإطار برتقالي. الخط الكهربائي أسود رفيع، والضوئي برتقالي سميك، واللاسلكي رمادي متقطع.
- **الـPlots:** محاور سوداء بلا إطار علوي وأيمن، وشبكة رمادية فاتحة جدًا، ووحدات على كل محور، ورقم على النقاط المهمة (مثل طول التعادل 90 m و181 m).
- **الصور الفوتوغرافية:** لم تُستخدم، لأن مواقع الصور (Wikimedia) محجوبة في بيئة العمل. يمكن إضافة صورة حقيقية لشريحة الحالة (ملعب Maracanã) أو لكابل ألياف إذا توفرت صورة بترخيص مناسب.

---

## G. الـAppendix (منفّذ في الملف)

| رقم | المحتوى |
|---|---|
| A1 | أنواع الـRAU (BBoF وIFoF وRFoF) مع DL وUL |
| A2 | Plot: BER مقابل CSR مع خط عتبة HD-FEC |
| A3 | مخطط عرض 5G + 6G البحثي |
| A4 | المراجع |

حساب CPRI والمصطلحات وجدول المعايير انتقلت إلى الـSpeaker Notes وإلى هذا التقرير (القسمان B وH).

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
CPRI: R = fs × 2 × N × 16/15 × line code. لحالة LTE 20 MHz (15-bit) الناتج 1228.8 Mb/s، وهو CPRI option 2. لحالة 100 MHz مع 64 هوائيًا الناتج ≈ 252 Gb/s قبل الـLine coding، أو ≈ 315 Gb/s مع 8B/10B (محسوب، وهي القيمة المرسومة في الشريحة 8). في A-RoF يشغل كل تيار هوائي تقريبًا عرض قناته الراديوية.
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
Carrying radio signals over optical fiber
Speaker A  ·  Speaker B  ·  15 minutes
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f01_title.png](Image 0)
1

### Notes:
0:20, Speaker A. Introduce the topic and the split: Speaker A covers problem, definition, signal path, architecture and RoF types; Speaker B covers the comparisons, limits, the deployment case and the conclusion.

<!-- Slide number: 2 -->
The problem
Large buildings and venues need many antenna points, fed from one equipment room.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f02_problem.png](Image 0)
2

### Notes:
1:00, Speaker A.
Outdoor macro signals are attenuated by walls and distance, so coverage inside tunnels, stadiums and large buildings is provided by many indoor antenna points.
The radio equipment is kept in one room (or a base-station hotel) to share power, cooling, maintenance and operator access.
The engineering question is therefore: how do we carry the radio signal from that room to each antenna point, over tens of metres to kilometres, within a loss, noise and distortion budget?
Scope: only this transport segment. Backhaul to the core network and air-interface design are out of scope.

<!-- Slide number: 3 -->
What RoF is
The radio waveform modulates light. A photodiode turns it back into the same radio signal.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f03_definition.png](Image 0)
Sources: ITU-T G.Suppl.55 (10/2025); ITU-T G.9803 (2018).
3

### Notes:
1:15, Speaker A.
Definition used in this talk: an optical link that carries an analog radio waveform, at RF or IF, with E/O conversion at one end and O/E at the other.
Read the spectra left to right: the RF signal at f_RF; after the laser, the optical carrier with two sidebands at ±f_RF; after the photodiode, the original RF signal again.
Key boundary: RoF transports a radio signal. It does not create spectrum or wireless capacity. Digitized I/Q transport (CPRI) is called digital fronthaul here, not RoF.

<!-- Slide number: 4 -->
Signal path: downlink and uplink
Four optical conversions in a two-way link. Each adds noise and distortion.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f04_signal_path.png](Image 0)
Source: C. H. Cox III, Analog Optical Links, Cambridge University Press, 2004.
4

### Notes:
1:30, Speaker A.
Downlink: base-station RF output → E/O at the central site → fiber → O/E at the remote unit → power amplifier → duplexer → antenna.
Uplink: antenna → duplexer → LNA → E/O at the remote unit → fiber → O/E at the central site → base-station RF input.
Downlink and uplink use separate fibers or separate wavelengths. WDM is optional; it is only needed when several links share one fiber.
With intensity modulation and direct detection, 1 dB of optical loss costs 2 dB of RF loss (square-law detection, Cox 2004). We use this on slide 7.

<!-- Slide number: 5 -->
Where it sits in the network
RoF is the fronthaul link from head-end to remote unit. Backhaul stays digital.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f05_architecture.png](Image 0)
5

### Notes:
1:15, Speaker A.
Operators' radios sit in a base-station hotel. The head-end combines their RF signals and converts them to optical (and back for the uplink).
Fibers run in a star to the remote antenna units (RAUs). The RAU is not passive: it contains photodiode, laser, amplifiers, filters and needs power.
Backhaul (base station to core) is a digital packet link and is not affected by the choice of RoF.
Because the analog link carries whatever RF is fed into it, several operators and bands can share it, within its bandwidth and dynamic range.

<!-- Slide number: 6 -->
Three ways to use the fiber
Simpler remote unit means analog signal on the fiber. Digital needs a full radio at the remote end.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f06_types.png](Image 0)
6

### Notes:
1:30, Speaker A. Hand over to Speaker B after this slide (about 7:00 elapsed).
RFoF: the fiber carries the radio signal at its final frequency. The remote unit only converts and amplifies. The optics must work at the carrier frequency.
IFoF: the fiber carries a lower intermediate frequency. The remote unit needs a mixer and local oscillator.
Digital fronthaul (CPRI): the fiber carries sampled I/Q bits. The remote unit is a complete radio with DAC, mixer and amplifier. This is not RoF, but it is the main alternative.
Trade-off: remote-unit complexity rises from top to bottom; fiber capacity requirement rises in the opposite direction (slide 8).

<!-- Slide number: 7 -->
Coax or fiber? It depends on length
Fiber has lower RF loss only beyond a break-even length set by the conversion loss.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f07_loss.png](Image 0)
Coax: Times Microwave LMR-400 datasheet (22.2 dB/100 m at 2500 MHz). Fiber: G.652.D cable datasheets. Conversion loss values are assumptions.
7

### Notes:
1:45, Speaker B.
Comparison defined: passive LMR-400-class coax versus an unamplified analog RFoF link, from the head-end RF port to the remote antenna port, downlink, 2.5 GHz.
Coax loss: 22.2 dB per 100 m (datasheet). Fiber: 0.25 dB/km optical, which is 0.5 dB/km in RF terms (panel a).
The RoF link also has a fixed RF-to-RF conversion loss. 20 dB and 40 dB are assumed values for illustration; the real value comes from the equipment datasheet.
Break-even length = conversion loss / (0.222 − 0.0005) dB/m: about 90 m and 180 m.
In practice both systems use amplifiers, so the deciding metrics become noise figure, dynamic range and power consumption, not loss alone.

<!-- Slide number: 8 -->
Analog RoF vs digital fronthaul
Digital fronthaul line rate grows with every antenna and every MHz of bandwidth.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f08_cpri.png](Image 0)
Source: CPRI Specification V7.0 (2015). Rates computed with the formula in the notes.
8

### Notes:
1:30, Speaker B.
CPRI rate = sample rate × 2 (I and Q) × 15 bits × 16/15 (control) × 10/8 (8B/10B line coding).
20 MHz LTE, one antenna: 30.72 Msps → 1228.8 Mb/s, which is CPRI option 2. 100 MHz NR at 122.88 Msps → 4.9 Gb/s per antenna, about 315 Gb/s for 64 antennas.
An analog link instead carries each antenna stream in roughly its radio bandwidth, so the fiber capacity needed is much smaller.
What analog gives up: quality degrades along the link (noise, distortion, dispersion), there is no bit-level monitoring, and interfaces are mostly vendor-specific. Digital links are robust and standardized (CPRI, eCPRI, O-RAN 7.2x).
eCPRI with split 7.2x reduces the digital rate; it scales with MIMO layers and traffic, not antenna count.

<!-- Slide number: 9 -->
Benefit: low fiber loss
Fiber loss is a fraction of a dB per km, and the fiber itself does not pick up interference.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f09_attenuation.png](Image 0)
Datasheet points: Prysmian G.652.D cable. Model curve is illustrative (Rayleigh scattering and infrared absorption).
9

### Notes:
1:00, Speaker B.
Standard single-mode fiber (G.652.D): cabled maximum around 0.36 dB/km at 1310 nm and 0.22 dB/km at 1550 nm (vendor datasheets). The curve is an illustrative physical model, the squares are datasheet limits.
Conditions on each benefit:
– Low loss matters only above the break-even length (slide 7).
– The fiber is immune to electromagnetic pickup; the remote electronics and the radio link are not.
– Central equipment is easier to share and maintain, but the remote unit still needs power.
– Cost is site-specific and is not claimed here.

<!-- Slide number: 10 -->
Limit 1: chromatic dispersion
At 1550 nm the received RF power fades at certain frequencies. Sub-6 GHz bands are barely affected.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f10_dispersion.png](Image 0)
Model: U. Gliese et al., IEEE Trans. Microwave Theory Tech. 44(10), 1996. Curves computed for standard SMF.
10

### Notes:
1:00, Speaker B.
With double-sideband intensity modulation, the two optical sidebands travel at slightly different speeds. After detection they interfere, and the RF power drops to zero at specific frequency–length combinations.
Computed with P ∝ cos²(π·L·D·λ²·f²/c), D = 17 ps/(nm·km). At 10 km the first null is near 19 GHz.
Mitigation: operate at 1310 nm (near-zero dispersion), use single-sideband modulation, or use IFoF.
This matters for mmWave over km-scale fiber, not for indoor sub-6 GHz systems.

<!-- Slide number: 11 -->
Limit 2: noise vs distortion
An analog link has a limited usable power window.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f11_sfdr.png](Image 0)
Too little signal
lost in noise
 
Too much signal
intermodulation appears
 
SFDR
the usable window between the two
Illustrative, no values. Source: C. H. Cox III, Analog Optical Links, 2004.
11

### Notes:
1:00, Speaker B.
Laser noise, photodiode shot noise and receiver thermal noise set a noise floor. Laser and modulator nonlinearity creates intermodulation, which rises 3 dB for every 1 dB of input.
The spurious-free dynamic range is the span between the two. It limits uplink sensitivity and how many carriers can share one link.
Other practical limits: one fiber pair or wavelength pair per remote unit, power needed at every remote unit, and no bit-level performance monitoring on an analog link.

<!-- Slide number: 12 -->
Case: Maracanã and Mineirão (2014)
Fiber-fed distributed antenna system for five operators, 2G / 3G / 4G.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f12_stadium.png](Image 0)
Sources: Axell Wireless press release, June 2014; RFS press release, 10 June 2014. Schematic only.
12

### Notes:
1:00, Speaker B.
Reported by the vendors: Axell Wireless (June 2014) supplied optical DAS for stadiums including Maracanã and Mineirão, combined capacity over 141,000, five operators, 2G/3G/4G. RFS (10 June 2014) supplied HYBRIFLEX hybrid fiber and DC power cable at Maracanã.
Not reported: link budgets, noise figures, measured capacity, cost comparison, or whether each subsystem carried analog RF or digital fronthaul.
So the case shows feasibility of a multi-operator fiber DAS in a large venue. It does not support performance or cost claims.
The figure is a schematic, not the real floor plan.

<!-- Slide number: 13 -->
When to choose analog RoF
RoF moves the antenna point closer to users. It does not add spectrum.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f13_decision.png](Image 0)
13

### Notes:
1:00, Speaker B.
Conclusions, each tied to a slide:
1. RoF transports an existing radio signal; it does not add spectrum or wireless capacity (slide 3).
2. Against passive coax, it has lower loss only beyond a break-even length (slide 7).
3. Against digital fronthaul, it needs far less fiber capacity and a simpler remote unit, at the cost of noise, distortion, dispersion and weaker monitoring (slides 8, 10, 11).
4. Documented use: multi-operator fiber DAS in large venues (slide 12).
The flow on the slide is the decision checklist that follows from these points.

<!-- Slide number: 14 -->
Questions
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/f01_title.png](Image 0)
14

### Notes:
Appendix slides cover RAU types, a measured BER curve, a 5G/6G research demo, and references.

<!-- Slide number: 15 -->
A1  Remote unit types
What the remote unit must contain for each signal on the fiber.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/a_rau.png](Image 0)
Redrawn from: Electronics 9(11), 1785 (2020), Fig. 3. DOI: 10.3390/electronics9111785.
15

### Notes:
BBoF here means analog baseband over fiber, as in the source figure. It is different from digital fronthaul.

<!-- Slide number: 16 -->
A2  Measured BER vs carrier-to-sideband ratio
One experimental link: 10 km fiber + 3 m wireless. Best result near 25 dB.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/a_csr.png](Image 0)
Redrawn from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 6. Values read from the published plot.
16

### Notes:
Values are approximate readings from the published plot (verification against the paper required). At low CSR distortion dominates; at high CSR noise dominates. The result applies only to the tested link.

<!-- Slide number: 17 -->
A3  Research demo: 5G + candidate 6G on one fiber
Laboratory demonstration, not a deployed system.
![/tmp/claude-0/-home-user-AboOmar12/e9733a54-4f82-5489-a2a7-ad29d271dc42/scratchpad/figs/a_demo.png](Image 0)
Redrawn and simplified from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 2.
17

### Notes:
The 6G branch uses a second laser and a UTC photodiode to generate a THz signal by optical beating. '6G' is the authors' label.

<!-- Slide number: 18 -->
A4  References
C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge University Press, 2004.
U. Gliese, S. Nørskov, T. N. Nielsen, Chromatic dispersion in fiber-optic microwave and millimeter-wave links, IEEE T-MTT 44(10), 1996.
ITU-T G.9803 (2018), Radio over fibre systems, with Amendments 1 (2019) and 2 (2022).
ITU-T G-series Supplement 55 (10/2025), Radio-over-fibre technologies and their applications.
ITU-T G.652, single-mode optical fibre and cable; Prysmian G.652.D cable datasheet.
CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).
Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, Analogue Radio Over Fiber for Next-Generation RAN, arXiv:2111.13851, 2021.
Radio over Fiber: An Alternative Broadband Network Technology for IoT, Electronics 9(11), 1785, 2020.
M. U. Hadi, G. Murtaza, Fibre Wireless Distributed Antenna Systems for 5G and 6G Services, Electronics 12(1), 64, 2023.
Times Microwave Systems, LMR-400 datasheet.
Axell Wireless press release, June 2014; RFS press release, 10 June 2014.
18
```
