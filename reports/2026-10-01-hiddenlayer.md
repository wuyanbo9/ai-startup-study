---
company: HiddenLayer
slug: hiddenlayer
date: 2026-10-01
layer: 应用
sector: 安全
growth_tier: 第一梯队
arr: 「数千万美元」且过去 12 个月 10x+（2026-09，官方口径，未给绝对数）；推算约 $30–50M
valuation: 未披露（2026-09-02 完成 $100M B 轮，公司明确不公布估值）
---

# HiddenLayer —— 向 AI 采用本身收一道过审税

## 📈 增长快照（先看这个）

| 项目 | 数据 |
|---|---|
| 成立时间 | 2022 年 3 月，美国得州奥斯汀；2022 年 7 月出 stealth `[媒体]` |
| 收入曲线 | 2022/07 出 stealth 收入为零 → 2025/09 约 $3–5M `[估算]` → 2026/09「数千万美元」，推算 $30–50M `[官方口径 + 估算]` |
| **增长倍数** | **过去 12 个月 10x 以上**（CEO Chris Sestito 原话，90% 以上的增长来自新客户）`[官方]` |
| 最新估值 | 未披露。2026-09-02 完成 $100M B 轮，Delta-v Capital 领投，累计融资 $156M `[官方]` |
| 团队规模 | 约 169 人（2026-05，第三方数据源）`[媒体]` |
| **人均创收** | 按 $35M 中值 ÷ 169 人 ≈ **$207K/人** `[估算]` —— 落在传统 SaaS 的 $150–250K 区间正中，没有任何 AI 人效溢价 |

**它凭什么长这么快：因为它的收入曲线不是自己的曲线，是客户的 AI 采用曲线。** 这家公司 2022 年 3 月就成立了，卖的东西三年基本没变——给企业自己部署的 AI 做资产清点、上线前扫描、持续攻击模拟和运行时拦截。真正变的是买方那一侧：2025 年下半年起 agent 开始进生产系统，提示注入、工具滥用、自主编码 agent 越权从论文里的东西变成了要上报的事件类别，于是企业内部那个「这个模型/这个 agent 能不能上线」的签字环节第一次有了专门的预算行。HiddenLayer 的产品在风来之前就造好了，所以风一来，12 个月净新增 50 多家平台客户、ARR 翻十倍以上，而其中 90% 以上来自全新客户——也就是说，它的增长几乎全部是「市场终于出现了」，而不是「老客户用得更多了」。

这句话的反面同样重要：一道税的税率由主体支出决定，而且主体平台有权把这道税自己收走。下面会反复回到这一点。

## 1. 核心产品

HiddenLayer 卖的是一个叫 AISec Platform 的企业平台，四个模块 `[官方]`：

- **AI Discovery**：自动清点企业内部所有 AI 资产——包括没人登记的 shadow AI。这是楔子，先告诉你「你有 300 个模型和 agent 在跑，你只知道 40 个」。
- **AI Supply Chain Security**：模型上线前扫描。开源权重文件本质是可执行的序列化对象（pickle 那一类），里面可以藏恶意代码、后门权重和未知组件，这个模块在模型进生产前把它拆开看。
- **AI Attack Simulation**：持续对自己的 AI 应用做对抗测试，号称覆盖 MITRE ATLAS 里的全部 64 类攻击手法 `[官方，2023 年口径]`。
- **AI Runtime Security**：生产环境里的实时检测与拦截。2026 年 B 轮之后新加的两块是 Agentic Runtime Security 和 Agent Harness Security，后者专门保护自主编码 agent——也就是 Cursor/Claude Code/Devin 这类工具在企业内网里跑起来之后的那个攻击面。

部署形态是**无探针、旁路、不接触训练数据、模型无关** `[官方]`。这一点要记住：它是产品宣传语，同时也是本篇最关键的弱点，后面第 2 节会用到。

**Before / After 的工作流差异**

| | Before | After |
|---|---|---|
| 谁来查 | 外聘顾问做一次 AI 红队，或者安全团队干脆禁止业务上线 AI | 平台常驻，接 CI/CD、SIEM/SOAR、API 网关、MLOps |
| 覆盖范围 | 一个应用 | 清点出来的全部 AI 资产 |
| 频次 | 一次，约四周 `[媒体]` | 持续 |
| 代价 | 一次 $16K–150K，报告交付即过期 `[媒体]` | 年费制，AWS Marketplace 挂牌全平台 $5M/年 `[媒体]` |
| 谁签字 | 没人敢签 | CISO 拿着一份可审计的控制项签字 |

它替代的既不是人也不是软件——**它替代的是「不批」**。在它出现之前，CISO 面对一个要上线的 AI 应用只有两个选项：花四周买一份一次性的顾问报告，或者拖着。这是理解它定价和天花板的全部钥匙。

## 2. 商业模式

- **收费对象**：CISO 办公室 / AI 治理委员会的预算。注意这不是 AI 团队的预算，也不是业务部门的预算——它是审批方的预算。行业调研显示 69% 的企业至今没有专门的 AI 安全预算行 `[媒体]`，这既解释了它为什么憋了三年，也解释了为什么一旦有了预算行，增长是台阶式的。
- **定价结构**：企业年费订阅，官网没有定价页 `[官方，查无]`。能查到的唯一公开标价在 AWS Marketplace：**$5,000,000 / 12 个月 / 单位，一个单位即全平台访问，不可退款不可取消**（第三方定价基准于 2026-09-05 核验）`[媒体]`。同一渠道上，做相邻品类的 Prompt Security 挂 $10,000 / 12 个月 / 维度 `[媒体]`——**同一个货架上 500 倍的价差**。这不是折扣策略的差异，这是一个还没谈妥计价单位的品类：按模型数？按 agent 数？按席位？按调用量？没人知道。
- **单位经济**：毛利未披露。但它不转售上游推理算力、不按 token 向前沿 API 付费（核心检测是自训模型加确定性静态分析），所以它的成本结构更接近传统安全软件而不是 AI 应用——毛利大概率在 75–85% `[估算，依据：无上游模型成本，主要成本是人力与云托管]`。真实的问题不在毛利，在人效：169 人做约 $35M，人均 $207K，和普通 SaaS 一模一样。
- **它从谁的预算里抢钱**：**既不是软件预算，也不是人力预算，而是 AI 项目预算的一个抽成**。这是本档里少见的第三类。它的上限既不是「原来买的那个软件多少钱」，也不是「原来雇的那些人多少钱」，而是「被卡住的那个 AI 项目有多大」。Gartner 的口径里，「保护 AI 本身」这个品类 2025 年全球约 $2.8B，2030 年预测 $16.4B；而「用 AI 做安全」那一块 2026 年就有 $48.5B、2030 年 $204.5B `[媒体，转述 Gartner 2026-08 预测]`。**它站在 12:1 里的那个 1 上面。**

**不可替代性（必答，且必须写短）**

| 问题 | 答案 |
|---|---|
| **自己造了什么** | 自研模型文件扫描器、39 项已授权专利（65 项在审）、公开披露 Policy Puppetry 的漏洞研究队 |
| **转手卖什么** | 基本不转售上游算力；运行时要搭在云网关与 SIEM 上，这部分占价值不足一成 `[估算]` |
| **抽掉 AI 还剩什么** | 一个静态文件扫描器、一个策略代理、一张国防与情报口的资质——是个漏洞研究所 |
| **换掉它要付什么** | 卸掉旁路探针、重跑一次资产清点；不留存数据、无资质门槛，数周可完成 |
| **上游原生做了会怎样** | 云厂商护栏已内置，六家安全平台已把同样四个模块打包进订阅——独立品类正在被消化 |

**不可替代性：弱。**

理由只有一条，但它是决定性的：**这个赛道的同行已经一家一家被平台厂商买走并变成了订阅里的一个勾选项。** Robust Intelligence 进了 Cisco AI Defense（2024）；Protect AI 以 $634.5M 被 Palo Alto 收购并成为 Prisma AIRS（2025-07-22 交割，数字来自 PANW 年报）；Lakera 约 $300M 被 Check Point 收走；Prompt Security 进 SentinelOne、Aim 进 Cato、Apex 进 Tenable `[媒体]`。HiddenLayer 这 $100M 买的是一张留在场上的票，不是一条护城河。

唯一真正黏的那部分是国防部、情报界和 DOE Prometheus 项目带来的资质与合同位置——但那块的增长形状像事务所，不像软件，而且它占不到大头：90% 以上的新增收入来自商业客户，而商业客户的切换成本按它自己的卖点算只有数周。

```model
{
  "domain":   "hiddenlayer.com",
  "founded":  "2022-03",
  "who":      {"label": "要上 AI 的企业安全负责人", "sub": "金融、大型科技、国防与情报；采购集中在少数几十家头部企业，2026 年 12 个月净新增 50+ 家"},
  "need":     "每一个新模型、每一个新 agent 上线都要过安全评审，但 CISO 手里没有任何能检查模型文件和 agent 行为的工具。69% 的企业连专门的 AI 安全预算行都没有。结果不是出事，而是卡住——一个季度能卡掉一整条 AI 路线图，而卡住的代价由业务部门承担、骂的是安全部门。",
  "before":   {"label": "外聘顾问做一次性 AI 红队，或者干脆不批", "pain": "一次红队 $16K–150K、约四周，只覆盖一个应用，报告交付当天就过期；而 AI 资产每周都在变，还有一半是没人登记的 shadow AI"},
  "solution": {"label": "把一次性评测改成常驻的四件事", "detail": "资产发现 + 上线前扫描模型文件 + 持续攻击模拟 + 运行时拦截，以无探针旁路接进 CI/CD 与 SIEM。把「一个应用、四周一次」改成「全部 AI 资产、持续」，把评审从一次采购变成一个可审计的控制项"},
  "payer":    {"label": "CISO 办公室 / AI 治理委员会", "buys": "买的不是防护效果，是让 AI 项目通过评审上线的那张签字；国防与情报口的客户另外买一层资质"},
  "why":      "参照价有两个，差了两个数量级，这正是问题所在。往下看：一次外聘 AI 红队 $35–55K，只管一个应用四周；往上看，它在 AWS Marketplace 的全平台年费挂 $5M。两者之间的差价不是按安全效果定的，是按被卡住的 AI 项目规模定的——一个企业级 AI 路线图延期一个季度，代价远超 $5M，所以这个价付得出来。但同一个货架上 Prompt Security 只挂 $10K/维度，500 倍价差说明这个品类连计价单位都没谈妥；计价单位不稳定的品类，一旦被平台厂商按零元捆绑，价格会直接塌。",
  "proof":    [
    {"k": "ARR 增速（官方）", "v": "过去 12 个月 10x 以上"},
    {"k": "ARR 绝对值", "v": "官方只说「数千万美元」，推算 $30–50M"},
    {"k": "新增中来自新客户", "v": "90% 以上"},
    {"k": "净新增平台客户", "v": "12 个月 50+"},
    {"k": "已授权专利", "v": "39 项（另 65 项在审）"},
    {"k": "人均创收", "v": "约 $207K（估算，169 人）"},
    {"k": "旗舰客户", "v": "一家周活 7 亿+ 的前沿模型厂商"}
  ],
  "catch":    "它卖的是「保护 AI」，而 Gartner 给这个品类 2030 年只有 $16.4B，是「用 AI 做安全」那块 $204.5B 的十二分之一。更要紧的是：赛道里六家同行已经分别被 Cisco、Palo Alto、Check Point、SentinelOne、Cato、Tenable 买走并打包进平台订阅，独立定价正在消失。它这 $100M 买的是留在场上的票。",
  "unit":     "年化收入（百万美元，含估算）",
  "timeline": [
    {"d": "2025-09", "v": 3.5, "label": "约 $3–5M（按官方「10x」反推，估算）", "mark": "曲线从这里折向上：2022-07 出 stealth 时收入为零，之后三年一直是平的；agent 开始进生产系统后，提示注入与工具滥用变成要上报的事件类别，CISO 的签字环节第一次有了专门预算行"},
    {"d": "2026-09", "v": 35, "label": "官方「数千万美元」，推算 $30–50M（估算）"}
  ]
}
```

## 3. 北极星指标

- **North Star（推断）**：**每个客户内部被纳管的 AI 资产数**（模型 + agent + 未登记的 shadow AI）。官方未披露任何内部指标，这是从产品结构倒推的：AI Discovery 是四个模块里唯一的楔子，先清点出三百个资产、再按资产谈扫描和运行时覆盖，整条扩张路径都挂在这个数上。
- **为什么是它**：它领先于收入两步。清点数先涨（装进去就涨），纳管率再涨（谈判出来的覆盖范围），收入最后涨（下一个续约周期）。而且它是唯一能向 CISO 证明「你比你想象的更暴露」的数字——这家公司的销售动作本身就是把这个数字摆到桌上。
- **配套指标**：
  1. **新客户数**，而不是净留存。官方说 90% 以上的增长来自新客户，意味着老客户扩张几乎不贡献——这个结构下公司内部盯的一定是新签数量。
  2. **攻击模拟发现的高危项修复率**。这是续约的唯一证据链：没有修复动作，年费就变成一份没人看的报告。
  3. **agent 侧资产占比**。Agent Harness Security 这条新 SKU 的成败就看这个比例能不能从个位数爬上来。
- 均为推断，官方未披露。

## 4. AI 在业务中的作用

| 层次 | 该公司的情况 |
|---|---|
| **AI = 产品本身** | **部分成立，但比宣传弱。** 保护的对象是 AI，但自己的核心能力里至少一半不是 AI：模型文件扫描是确定性静态分析（序列化对象反编译、后门权重比对），策略拦截是规则代理。真正是 AI 的是运行时的提示注入/异常行为分类器，自训。 |
| **AI = 效率杠杆** | **几乎不成立。** 169 人做约 $35M、人均 $207K，和普通 SaaS 无异。它没有用 AI 把自己做小，它只是用 AI 把别人的风险做成了商品。 |
| **AI = 营销标签** | **这是占比最大的一层，但方式特殊。** 它的增长和自身技术进步没有因果关系，和客户买了别人的 AI 有因果关系。CEO 自己说得很直白：「推理还是推理，我们没有转型，只是不断扩大范围」——从预测式 ML 到生成式再到 agent。产品没变，标签换了三轮，市场终于来了。 |

**自研还是调 API**：核心检测不调前沿模型 API，强调无探针、不接触训练数据。模型层依赖风险因此很低——但硬币的另一面是，**它也拿不到前沿模型升级的红利**。别人每次模型变强都能顺势涨能力，它不能。

**基础模型升级对它是利好还是威胁**：短期明确利好。每一轮新能力都是一个新攻击面，也就是一个新 SKU——Agent Harness Security 这条产品线完全是编码 agent 普及催出来的。但中期是威胁，而且不是来自模型厂商的护栏，是来自安全平台：当 Prisma AIRS、Cisco AI Defense、Check Point（Lakera）都把同样四个模块装进已经签了的平台合同里，HiddenLayer 要让客户为同一件事再开一张单独的采购单。

值得单独记一笔的悖论：2025 年 4 月它自己公开披露了 Policy Puppetry——一种把对抗指令伪装成 XML/JSON/INI 结构化「系统策略」的通用提示注入技术，无需针对特定模型调参，绕过了 OpenAI、Google、Microsoft、Anthropic、Meta、DeepSeek、Qwen、Mistral 全部主流模型的安全对齐 `[媒体]`。作为漏洞研究这是顶级的权威证明，作为商业叙事它很尴尬：一家卖防护的公司向全世界证明了这个问题目前无解。买家下一个问题必然是——那我买了之后到底拦住了什么？

## 5. 增长引擎

主引擎是 **SLG 加上一个由并购造出来的真空**，这条很少见，值得说清：

1. **「买不到的那一家」本身是销售卖点。** 头部同行被一家家买走之后，想要一个不绑在某家安全平台上的中立 AI 安全供应商，可选项急剧收缩。对于已经买了 Palo Alto 又不想在 AI 安全上被同一家锁死的大企业，HiddenLayer 的独立身份是采购理由。
2. **云市场渠道绕过采购流程。** 在 AWS / Azure Marketplace 上挂牌，企业可以用已承诺的云消费额度抵扣（EDP burn-down），不走新供应商准入那一套。这也是它唯一公开过价格的地方。
3. **漏洞研究做顶部漏斗。** Policy Puppetry 这种全模型通用绕过的公开披露，是不花钱的权威认证，直接把 CISO 拉进对话；叠加 Gartner AI 安全 Cool Vendor 的背书。
4. **政府口既是收入也是资质。** 国防部与情报界合同，2026-08-18 入选能源部 Genesis Mission 下的 Prometheus 计划（$60M/三年、20+ 产业伙伴、与 Idaho National Labs 搭档）`[官方]`。注意：是 20 多家伙伴分这 $60M 的三年额度，**不等于它的收入**。
5. **投资人名单就是渠道表。** 两轮里出现的 Booz Allen Hamilton（联邦集成商）、M12、Morgan Stanley、IBM、Capital One —— 全是客户型投资人。B 轮还新聘了 CRO Mike Gesnaldo 专攻欧洲与 EMEA 渠道 `[官方]`。

缺的那条：没有 PLG。无免费档、无开源版、无自助注册，一切都走企业销售。这就是为什么 169 人才能做 $35M。

## 6. 风险与争议

1. **整个品类正在被吞并，它是最后一个站着的大个子。** 六家同行的成交价区间是 $300M–$634.5M——这是「平台的一个功能模块」的定价，不是「一家公司」的定价。而 HiddenLayer 这轮 $100M **明确不披露估值**。在一个有如此清晰可比成交价的赛道里选择不披露，通常不是好消息。
2. **TAM 被 Gartner 按在 12:1 的小头上。** 「保护 AI」2030 年 $16.4B，「用 AI 做安全」$204.5B。前者还要被六家平台厂商和 Noma、Zenity、Straiker 这些仍在融资的同行分。
3. **收入质量：90% 以上的新增来自新客户。** 这个数字官方是当成绩说的，但它同时意味着老客户扩张对增长几乎没有贡献。叠加「AI 治理」这类预算常见的一次性项目属性，这是一条「每年都要重新打一遍」的收入曲线。净留存率一次都没公布过。
4. **价格体系没有共识。** 同一个云市场货架上 $5M 和 $10K 并存，500 倍。计价单位未定的品类，定价权在买方和捆绑者手里，不在它手里。
5. **它自己的研究证明了防线是漏的。** 见上节 Policy Puppetry 悖论。这个赛道卖的是信心，而最硬的研究成果恰恰在削弱信心。
6. **人效不支持 AI 公司的估值叙事。** 人均 $207K、绝对体量「数千万」，不到同为安全赛道的 Cyera（约 $150M，2026-05）的四分之一——而 Cyera 已经被本档批评过人均只有 $100K。换句话说，它在安全赛道里人效不差，但在 AI 创业样本里毫无特殊之处。
7. **旗舰客户与政府依赖的双重集中。** 一家周活 7 亿以上的前沿模型厂商是公开提及的旗舰客户——这类客户恰恰是最有能力自建的那类。政府侧合同受预算周期和政权更替影响，Prometheus 的 $60M 还要在 20 多家之间分。

## 7. 给我的启发

1. **最好的「卖铲子」位置未必在 AI 里，可能在 AI 的审批环节。** HiddenLayer 的收入曲线和自己的技术进步基本无关，和客户的 AI 采用率强相关——它的北极星其实是别人的采用曲线。这类生意识别起来有个特征：**产品三年没变，市场突然来了**。但同一个逻辑也框死了它的天花板：一道附加税的税率由主体支出决定，而且主体平台随时有权把这道税自己收走。找这类机会时，第一个要问的不是「税基有多大」，而是「谁有权把这道税并掉」。
2. **「造好了等风来」是真实的模式，但要查等待期的代价和风来时的独占性。** 本档已经有 n8n（六年 $7M 再到 $110M）、Speak（九年等语音模型）、Modal（四年前开始造容器运行时）、RADAR（13 年 RFID 硬件）四个同形状的样本。HiddenLayer 是第五个，但它的结局不同：前四家风来时手里的东西是独占的，HiddenLayer 风来时六家平台厂商直接花钱买了竞品补位。所以「等到了没有」不是关键问题，**「等待期烧掉的股权换来的东西，风来时还独占吗」才是**。
3. **判断不可替代性时，最便宜也最准的办法是先查同行的并购价。** 这个赛道同行的成交价是 $300M–634M，统一落在「平台的一个功能模块」那一档，而独立者刚融 $100M 且不披露估值。当一个品类的头部资产都以功能模块的价格被买走时，市场已经把结论写出来了：**它是功能，不是公司。** 能保持独立的，只有上游买不起或者买不到的东西——而「无探针、数周可卸、不接触数据」这三条产品优点，正好是「买得起、也买得到」的另一种说法。

## 来源

- [HiddenLayer Raises $100M Series B to Advance AI Security](https://www.hiddenlayer.com/news/hiddenlayer-100m-series-b-ai-security) — 2026-09-02（官方：10x+ ARR、50+ 新增平台客户、39 项授权专利 / 65 项在审、7 亿周活的前沿模型厂商客户）
- [HiddenLayer nabs $100M as enterprises rush to secure their AI deployments](https://techcrunch.com/2026/09/02/hiddenlayer-nabs-100m-as-enterprises-rush-to-secure-their-ai-deployments/) — 2026-09-02（CEO 口径「数千万美元、90% 来自新客户」、客户行业、竞争格局）
- [HiddenLayer raises $50M for its AI-defending cybersecurity tools](https://techcrunch.com/2023/09/19/hiddenlayer-raises-50m-for-its-ai-defending-cybersecurity-tools/) — 2023-09-19（Cylance 起源、MITRE ATLAS 64 类、2023 年 50 人）
- [HiddenLayer 公司资料（成立时间与创始人）](https://github.com/api-evangelist/hidden-layer) — 2026（2022 年 3 月成立，Sestito / Burns / Ballard）
- [HiddenLayer AISec Platform 产品页](https://hiddenlayer.com/aisec-platform/) — 2026（四模块、无探针、不接触训练数据）
- [AI Security Pricing Transparency Benchmark (2026)](https://aisecurityplatform.com/research/ai-security-pricing-transparency-2026/) — 2026（AWS Marketplace $5M/年全平台）
- [What AI Security Actually Costs in 2026](https://accuroai.co/blog/what-ai-security-actually-costs) — 核验于 2026-09-05（$5M/12 个月/单位、不可退不可撤；Prompt Security $10K/维度）
- [Which cybersecurity startup is growing the fastest?](https://newmarketpitch.com/blogs/news/cybersecurity-growing-startup) — 2026-09（HiddenLayer 列首位；Cyera $150M+ 对照）
- [Gartner's AI-amplified security forecast ($204B by 2030)](https://softwarestrategiesblog.com/2026/08/17/gartner-ai-amplified-security-forecast-204b-2030/) — 2026-08-17（保护 AI 2030 年 $16.4B vs AI 增强安全 $204.5B）
- [Gartner's $244.2B security forecast](https://softwarestrategiesblog.com/2026/03/24/information-security-spending-2026/) — 2026-03-24（2025 年保护 AI 约 $2.8B，17 倍不对称）
- [The Enterprise AI Security Benchmark Papers](https://securityboulevard.com/2026/07/the-enterprise-ai-security-benchmark-papers-how-leading-cisos-are-managing-ai-risk/) — 2026-07（69% 无专门 AI 安全预算行、62% 认为 agent 权限是最大问题）
- [Palo Alto Networks FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1327567/000132756725000027/panw-20250731.htm) — 2025（Protect AI 收购总对价 $634.5M，2025-07-22 交割）
- [Check Point acquires Lakera for $300 million](https://www.ynetnews.com/business/article/bksoa0dogl) — 2026（Lakera 约 $300M；Cato 收 Aim、SentinelOne 收 Prompt Security、Tenable 收 Apex）
- [Noma Security Raises $100 Million for AI Security Platform](https://www.securityweek.com/noma-security-raises-100-million-for-ai-security-platform/) — 2026（同赛道仍在融资的独立玩家）
- [All Major Gen-AI Models Vulnerable to 'Policy Puppetry' Prompt Injection Attack](https://www.securityweek.com/all-major-gen-ai-models-vulnerable-to-policy-puppetry-prompt-injection-attack/) — 2025-04（通用提示注入，覆盖全部主流模型）
- [AI Red Teaming Pricing 2026](https://security.aivyuh.com/blog/ai-red-teaming-pricing-2026/) — 2026（一次性红队 $8K–150K+，全栈四周 $35–55K）
- [HiddenLayer Selected to Support DOE's $60 Million Prometheus Initiative](https://www.prnewswire.com/news-releases/hiddenlayer-selected-to-support-does-60-million-prometheus-initiative-under-the-genesis-mission-302853514.html) — 2026-08-18（Genesis Mission 首个 Phase II、20+ 产业伙伴、Idaho National Labs）
- [HiddenLayer 融资与团队规模（第三方数据）](https://app.dealroom.co/companies/hiddenlayer) — 2026（$6M 种子 2022-07、$50M A 轮 2023-09、约 169 人）
