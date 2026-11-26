// 书籍排版模板，供各册共用
// meta 由 build.py 生成的 main.typ 传入

#let accent = rgb(meta.at("accent", default: "#1f4e79"))
#let body-font = ("Times New Roman", "SimSun")
#let head-font = ("Microsoft YaHei", "SimHei")
#let mono-font = ("Consolas", "SimSun")

#set document(title: meta.title, author: meta.author, keywords: meta.at("keywords", default: ()))
#set page(
  width: 170mm,
  height: 240mm,
  margin: (x: 20mm, top: 24mm, bottom: 22mm),
  numbering: "1",
)
#set text(font: body-font, size: 10.5pt, lang: "zh", region: "cn")
#set par(justify: true, first-line-indent: (amount: 2em, all: true), spacing: 0.9em, leading: 0.95em)
#set list(indent: 1.2em, spacing: 0.4em)
#set enum(indent: 1.2em, spacing: 0.4em)
#set block(spacing: 0.9em)

// 页眉页脚
#set page(header: context {
  let hs = query(heading.where(level: 1).before(here()))
  let chap = if hs.len() > 0 { hs.last().body } else { "" }
  set text(size: 8pt, fill: rgb("#8a8a8a"))
  grid(
    columns: (1fr, auto),
    align: (left, right),
    meta.title,
    chap,
  )
  v(-2mm)
  line(length: 100%, stroke: 0.4pt + rgb("#cfcfcf"))
})
#set page(footer: context {
  set text(size: 9pt, fill: rgb("#777777"))
  align(center, counter(page).display())
})

// 标题
#show heading: set text(font: head-font, fill: rgb("#1a1a1a"))
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(4mm)
  block(width: 100%)[
    #text(size: 18pt, weight: "bold", font: head-font)[#it.body]
    #v(3.2mm)
    #line(length: 100%, stroke: 1.4pt + accent)
  ]
  v(6mm)
}
#show heading.where(level: 2): it => block(above: 1.5em, below: 0.7em, width: 100%)[
  #text(size: 14pt, weight: "bold", font: head-font, fill: rgb("#1a1a1a"))[#it.body]
]
#show heading.where(level: 3): it => block(above: 1.1em, below: 0.5em, width: 100%)[
  #text(size: 11.5pt, weight: "bold", font: head-font, fill: rgb("#333333"))[#it.body]
]

// 目录
#show outline.entry: it => {
  set text(size: 10pt)
  link(it.element.location(), grid(
    columns: (auto, 1fr, auto),
    column-gutter: 0.6em,
    it.indented(it.prefix(), it.body()),
    repeat(gap: 0.15em)[.],
    it.page(),
  ))
}

// 插图
#show figure.where(kind: image): set figure(supplement: none, gap: 2.5mm)
#show figure.where(kind: table): set figure(supplement: none, gap: 2.5mm)
#show figure: set block(breakable: false)
#show figure.caption: it => block(above: 2mm, below: 4mm)[
  #set text(size: 9pt, fill: rgb("#444444"))
  #it
]
#show figure.where(kind: image): set figure.caption(position: bottom)
#show figure.where(kind: table): set figure.caption(position: top)

// 表格
#show table: set table(stroke: (top: 0.9pt, bottom: 0.9pt, rest: none), inset: (x: 4pt, y: 3.5pt))
#show table.cell.where(y: 0): set text(weight: "bold")
#set table(align: (auto, auto))

// 引用块
#show quote.where(block: true): it => block(
  width: 100%,
  fill: rgb("#f4f6f8"),
  inset: (x: 5mm, y: 3mm),
  radius: 2pt,
  stroke: (left: 2pt + accent),
)[#set par(first-line-indent: 0pt)
  #it.body]

// 代码
#show raw.where(block: true): it => block(
  width: 100%,
  fill: rgb("#f6f8fa"),
  inset: 7pt,
  radius: 3pt,
  stroke: 0.4pt + rgb("#e3e3e3"),
)[#set text(font: mono-font, size: 8.5pt)
  #it]

// 链接
#show link: set text(fill: accent)

// 强调
#show strong: set text(weight: "bold")

// 封面
#let cover-page() = page(
  margin: 0pt,
  numbering: none,
  header: none,
  footer: none,
  background: image(meta.cover, width: 100%, height: 100%, fit: "cover"),
)[
  #place(top + left, dx: 18mm, dy: 20mm)[
    #text(size: 9pt, fill: rgb(255, 255, 255, 200), tracking: 0.35em)[WHOLE BRAIN SIMULATION]
  ]
  #place(bottom + left, dx: 0pt, dy: 0pt, rect(
    width: 170mm,
    height: 118mm,
    fill: gradient.linear(
      rgb(0, 0, 0, 0), rgb(0, 0, 0, 199), rgb(0, 0, 0, 230),
      angle: 90deg,
    ),
  ))
  #place(bottom + left, dx: 18mm, dy: -74mm)[
    #text(size: 8.5pt, fill: rgb(255, 255, 255, 210), tracking: 0.18em)[
      #meta.series　·　第 #meta.volume 册
    ]
  ]
  #place(bottom + left, dx: 18mm, dy: -58mm)[
    #text(size: 30pt, weight: "bold", fill: white, font: head-font)[#meta.title]
  ]
  #place(bottom + left, dx: 18mm, dy: -42mm)[
    #text(size: 12.5pt, fill: rgb(255, 255, 255, 225), font: head-font)[#meta.subtitle]
  ]
  #place(bottom + left, dx: 18mm, dy: -24mm)[
    #text(size: 10.5pt, fill: rgb(255, 255, 255, 215))[#meta.author]
    #h(6mm)
    #text(size: 10.5pt, fill: rgb(255, 255, 255, 150))[#meta.year]
  ]
]

// 扉页
#let title-page() = page(
  numbering: none,
  header: none,
  footer: none,
)[
  #v(30mm)
  #align(center)[
    #text(size: 9pt, fill: rgb("#777777"), tracking: 0.25em)[#meta.series]
    #v(6mm)
    #text(size: 24pt, weight: "bold", font: head-font)[#meta.title]
    #v(4mm)
    #text(size: 13pt, fill: rgb("#444444"), font: head-font)[#meta.subtitle]
    #v(10mm)
    #line(length: 28mm, stroke: 1pt + accent)
    #v(10mm)
    #text(size: 11pt)[#meta.author]
    #v(3mm)
    #text(size: 10pt, fill: rgb("#666666"))[#meta.year]
  ]
]

// 版权页
#let copyright-page() = page(
  numbering: none,
  header: none,
  footer: none,
)[
  #v(1fr)
  #set par(first-line-indent: 0pt, justify: false)
  #set text(size: 8.5pt, fill: rgb("#555555"))
  #meta.title
  #linebreak()
  #meta.subtitle
  #linebreak()
  #linebreak()
  作者　#meta.author
  #linebreak()
  版本　2026 年 11 月
  #linebreak()
  #linebreak()
  本书文字与插图采用 CC BY-NC-SA 4.0 许可发布，转载请注明作者与出处。
  #linebreak()
  书中引用的论文、数据集与模型归各自作者所有。
]

// 正文起始
#let mainmatter() = {
  counter(page).update(1)
  include meta.body
}

// 封底
#let back-page() = page(
  margin: 0pt,
  numbering: none,
  header: none,
  footer: none,
  background: image(meta.back, width: 100%, height: 100%, fit: "cover"),
)[
  #place(top + left, dx: 0pt, dy: 0pt, rect(
    width: 170mm,
    height: 160mm,
    fill: gradient.linear(
      rgb(0, 0, 0, 217), rgb(0, 0, 0, 89), rgb(0, 0, 0, 0),
      angle: 90deg,
    ),
  ))
  #place(top + left, dx: 18mm, dy: 22mm)[
    #text(size: 9pt, fill: rgb(255, 255, 255, 200), tracking: 0.3em)[#meta.series]
    #v(5mm)
    #block(width: 110mm)[
      #text(size: 11pt, fill: rgb(255, 255, 255, 230))[#meta.blurb]
    ]
    #v(6mm)
    #text(size: 9.5pt, fill: rgb(255, 255, 255, 190))[#meta.author　·　#meta.year]
  ]
]
