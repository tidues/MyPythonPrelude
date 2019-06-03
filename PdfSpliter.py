import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from pyprelude import FilesGlob as fg
from pyprelude import NumberFuncs as nf

def splitPdf(fname, length):

    # get file base name without surfix
    fbname = os.path.splitext(os.path.basename(fname))[0]

    # read the pdf
    pdf = PdfFileReader(fname)

    # get page lists
    pageNum = pdf.getNumPages()
    docDict = nf.numberMod(range(pageNum), length)

    # split to new pdf
    for doc in docDict:

        pgLst = docDict[doc]
        pdf_writer = PdfFileWriter()

        for pg in pgLst:
            pdf_writer.addPage(pdf.getPage(pg))

        # write the pdf file
        ofname = '{}_{}_{}.pdf'.format(fbname, doc[0]+1, doc[1]+1)

        with open(ofname, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(ofname))


if __name__ == '__main__':
    fname = './DOC052219-05222019173825.pdf'
    splitPdf(fname, 12)

