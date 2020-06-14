using Weave
using Mustache

println("Hello World")

filename = normpath(Weave.EXAMPLE_FOLDER, "FIR_design.jmd")

weave(filename, out_path = "FIR")

weave("ex.jmd", out_path = "ex")

weave("ex.jmd", out_path = "ex2", doctype = "md2pdf")

# Julia markdown to Pandoc markdown
weave(filename; doctype = "pandoc", out_path = "FIR2")

#weave(filename; doctype = "pandoc2pdf", out_path = :pwd)

# filename = normpath(Weave.EXAMPLE_FOLDER, "FIR_design.jmd")
# weave(filename, fig_path = "figures", fig_ext = nothing,
#     cache_path = "cache", cache=:off, out_path = "res", doctype = "md2pdf")

# run(`pdflatex FIR_design.tex`)
