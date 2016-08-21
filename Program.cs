using System;
using System.IO;
using System.Linq;
using System.Text;
using iTextSharp.text.pdf;
using iTextSharp.text.pdf.parser;
using Microsoft.Office.Interop.Word;
using static System.IO.Path;

namespace GovermentParser
{
    internal class Program
	{
	    private const string InputDir = @"c:\ML\docs\";
		private const string OutDir = @"c:\ML\docs_out\";

	    public static void Main(string[] args)
		{
			ProccessWord();
			ProccessPdf();
		}

		private static void ProccessWord()
		{
			Application app = new Application();
			foreach (var file in Directory.GetFiles(InputDir, "*.doc").Where(x => !File.Exists(Combine(OutDir, GetFileName(x) ?? string.Empty))))
			{
                try {
                    var doc = app.Documents.Open(file);
                    var documentContent = new StringBuilder();
                    foreach (Paragraph paragraph in doc.Paragraphs)
                    {
                        var text = paragraph.Range.Text;
                        if (!string.IsNullOrEmpty(text) && !string.IsNullOrWhiteSpace(text))
                            documentContent.AppendLine(text);
                    }
                    Console.WriteLine(file);
                    File.WriteAllText(Combine(OutDir, GetFileName(file) + ".txt"), documentContent.ToString());
                    doc.Close();
                }
                catch (Exception)
                {
                    // ignored
                }
			}
			app.Quit();
		}

		private static void ProccessPdf()
		{
			foreach (var file in Directory.GetFiles(InputDir, "*.pdf").Where(x => !File.Exists(Combine(OutDir, GetFileName(x) ?? string.Empty))))
			{
				try
				{
					PdfReader pdfReader = new PdfReader(file);

					var documentContent = new StringBuilder();
					for (int page = 1; page <= pdfReader.NumberOfPages; page++)
					{
						ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
						string currentText = PdfTextExtractor.GetTextFromPage(pdfReader, page, strategy);

						var text = Encoding.UTF8.GetString(Encoding.Convert(Encoding.Default, Encoding.UTF8, Encoding.Default.GetBytes(currentText)));
						if (!string.IsNullOrEmpty(text) && !string.IsNullOrWhiteSpace(text))
							documentContent.AppendLine(text);
					}
					pdfReader.Close();

					Console.WriteLine(file);
					File.WriteAllText(Combine(OutDir, GetFileName(file) + ".txt"), documentContent.ToString());
				}
				catch (Exception ex)
				{
				    Console.WriteLine($"Error: {ex.Message}. {file}");
				}
			}
		}
	}
}
