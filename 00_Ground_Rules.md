# Pax Forecast Model: Ground Rules & Conventions

**Author:** Yash Moitra
**Institution:** Delhi International Airport Limited
**Date:** June 23, 2026

These conventions govern every document, dataset, script, and exhibit in the Pax
Forecast Model project. They are binding on all subsequent steps.

## Rule 1 - Variable Name List

A single living registry of variable names is maintained at `Variable_Names.md`. Every
variable used anywhere in the model must appear there with its meaning, class/domain,
example, and the step in which it is first defined. The list is updated as relevant as the
model is built: whenever a step introduces or changes a variable, that same step updates
the registry.

## Rule 2 - Definitions List

A single living registry of definitions is maintained at `Definitions.md`, covering every
domain term, abbreviation, and concept used in the model. It follows the same
update-as-we-go discipline as Rule 1.

## Rule 3 - Captioning & Numbering

Every formula, table, image, diagram, equation, drawing, lemma, assumption, graph,
corollary, and theorem is captioned and numbered, sequentially within each class in order
of first appearance: Equation (1), (2), ...; Table 1, 2, ...; Figure 1, 2, ... (images,
diagrams, drawings, graphs); and the theorem-like statements Assumption, Theorem, Lemma,
Corollary, each in its own sequence.

Theorem-like statements are set as a bold label and number followed by a period, then the
statement in italics, for example:

**Assumption 1.** *the statement.*

Variant labels may be primed (for example **Assumption 2'.**) and custom labels are
allowed (for example **Assumption C.**). Each exhibit is referred to by its label (for
example "by Equation (1)" or "by Assumption 1"), and cross-references to a numbered
statement are hyperlinked to it. A running index of all exhibits is kept in
`Methodology.md`.

## Rule 4 - Authorship & Dating

Every document is authored by **Yash Moitra, Delhi International Airport Limited**. Dates
are written as **Month DD, YYYY** with a zero-padded day (for example July 03, 2021). The
date carried by a document is its actual date.

## Rule 5 - Methodology Document

`Methodology.md` meticulously documents every step of the model: objective, inputs,
assumptions, procedure, decisions and their rationale, data treatments and gaps, outputs,
and verification. No material step occurs in the model without a corresponding methodology
entry.

## Rule 6 - No em dashes

Em dashes are not permitted in any project document. Where a sentence break or
parenthetical is needed, use a comma, colon, semicolon, parentheses, or a hyphen instead.

## Rule 7 - Typography and generation

Formatted documents use the standard CMU (Computer Modern) font family, both serif and
sans serif. Generation and knitting are done through a LaTeX engine wherever practical, so
that formatting stays consistent. PDF rendered via LaTeX in Computer Modern is the
preferred formatted output.

## Rule 8 - Title page

Every document opens with a title page. The date, written Month DD, YYYY and set in
Calibri, sits at the top left. The project title, identical across all documents, is set
large and bold (Checks-in, and Balances: a Matter of Time). Immediately beneath it, in small bold type, is
the document's own name (Overview, Ground Rules, Methodology, and so on). The author line
reads Yash Moitra in italics, carrying a superscript dagger that corresponds to a matching
dagger on the affiliation footnote. The affiliation, Delhi International Airport Limited, is
set in small type at the foot of the page. All text other than the date is set in Computer
Modern.

## Rule 9 - Contents page and numbering hierarchy

Every document carries a Contents page immediately after the title page. Top-level
sections are numbered with upper-case Roman numerals (I, II, III, ...) and shown in bold.
Subsections are numbered within their section as the section numeral, a dot, and a
two-digit zero-padded index (I.01, I.02, ..., III.27), shown with a colon before the title
and dotted leaders to the page number. A running footer carries the author (Moitra, Yash)
at the left, the page and total (for example i / 155) at the centre, and the month and
year at the right.

## Rule 10 - PDF knitting default for R Markdown

Every R Markdown (`.Rmd`) document defaults to knitting to PDF. Its YAML header declares
`output: pdf_document` as the first and default output, rendered through a LaTeX engine (per
Rule 7), so that knitting produces a PDF directly, with no extra steps and no manual format
selection. PDF is the only intended default target: HTML, Word, and the intermediate
`.knit.md` are never the deliverable. Every new `.Rmd` follows this from creation.

---

*Maintenance note:* the registries (Rules 1 and 2) are not pre-filled speculatively. Each
step records the variables and terms it actually introduces, at the point it introduces
them.
