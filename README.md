# HackMIT

Current Stack:
- OpenCV to get the images
- This [repository](https://github.com/lukas-blecher/LaTeX-OCR) to get detections. Simply run the command `pix2tex` and drop the image


Other Options that were explored during the hackathon:

Image to LateX:
- Mathpix (really good, but it's paid...)
- Pytesseract (Developed by Google. Works for normal text, but cannot detect LaTeX code)
- https://github.com/harvardnlp/im2markup

https://openai.com/blog/grade-school-math/
- https://github.com/openai/grade-school-math

1. Generate math problems / get the appropriate dataset
- https://mathy.ai/

- latex -> to solution
	- Trying to parse the LaTeX expression using Regex would be an absolute nightmare. When we look at a LaTeX expression, we don't actually think about these concepts in terms of the literal characters that make them up.
like $\int x^2dx$
- OpenAI solution with grade-school-math (comprehension problem)

Tool to help teachers.
- Special cases: Partial fractions, complex number, RREF for linear algebra, complex numbers, complex logic,  Baye's Rules,  simplify, 

Frontend / Backend
- Get the VR visualization, display a series of text as the answer to the problem. (Don't do mobile app because that has already been done, but rather do VR/AR).

For derives and integrals, you can plot the function.

Other pictures

Rather, we think at a more abstract level in terms of X.

### Installation
For Mac, make sure to have `Rust` installed by doing `brew install rust`. 




#### Installing Tesseract
We need Tesseract to convert the image to text.

On Linux
```bash
sudo apt-get update
sudo apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
```
On Mac
```bash
brew install tesseract
```
On Windows
download binary from https://github.com/UB-Mannheim/tesseract/wiki. then add pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' to your script.

Then you should install python package using pip:
```
pip install tesseract
pip install tesseract-ocr
```

```
brew install tesseract-ocr-eng
```