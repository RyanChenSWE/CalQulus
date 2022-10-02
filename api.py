from pprint import pprint
import requests
import urllib.parse
import ast
from sympy import preview, sympify, latex
from decouple import config
from pytexit import py2tex as p2t

### FUNCTIONS ###

def matrixConvert(s):
    s = '[[' + s[s.index('}') + 1:].replace("&", ",").replace('\\\\', '],[').replace(' ', '')
    return s[:s.index('\\')] + ']]'

# CONSTANTS ### 
appid = config('WOLFRAM_ALPHA_APP_ID')
MAX_CHARACTERS = 200

def latexSolver(query): 
  # check if there's an equal sign between two strings
  if '=' in query:
    # add 'solve' to the beginning of the query
    query = 'solve ' + query
  query = urllib.parse.quote_plus(query)
  query_url = "http://api.wolframalpha.com/v2/query?" \
              f"appid={appid}" \
              f"&input={query}" \
              "&podstate=Result__Step-by-step+solution" \
              "&format=plaintext" \
              "&output=json"

  r = requests.get(query_url).json()["queryresult"]

  # pprint(r)

  # check if a pod contains id "Result"
  if any(pod["id"] == "Result" for pod in r["pods"]):

      # get the pod with id "Result"
      result_pod = next(pod for pod in r["pods"] if pod["id"] == "Result")

      # return all plaintexts in the pod joined together, replace all round brackets with curly brackets
      return "\n".join(subpod["plaintext"] for subpod in result_pod["subpods"]).replace('(', '{').replace(')', '}')
  else:
      # get results pod
      results_pod = list(filter(lambda x: x['numsubpods'] > 0 and x['subpods']
                                [0]['plaintext'] != '', r['pods']))[0]['subpods'][0]['plaintext']

      if (len(results_pod) == 0):
          return "No steps shown."
      else:
          return results_pod.replace('(', '{').replace(')', '}')

class LatexVisitor(ast.NodeVisitor):

    def prec(self, n):
        return getattr(self, 'prec_'+n.__class__.__name__, getattr(self, 'generic_prec'))(n)

    def visit_Call(self, n):
        func = self.visit(n.func)
        args = ', '.join(map(self.visit, n.args))
        if func == 'sqrt':
            return '\sqrt{%s}' % args
        elif func == 'log':
            return '\log_{%s}' % args
        elif func == '±':
            return '\pm'
        else:
            # return pure string if not parseable
            return r'\operatorname{%s}\left(%s\right)' % (func, args)

    def prec_Call(self, n):
        return 1000

    def visit_Name(self, n):
        return n.id

    def prec_Name(self, n):
        return 1000

    def visit_UnaryOp(self, n):
        if self.prec(n.op) > self.prec(n.operand):
            return r'%s \left(%s\right)' % (self.visit(n.op), self.visit(n.operand))
        else:
            return r'%s %s' % (self.visit(n.op), self.visit(n.operand))

    def prec_UnaryOp(self, n):
        return self.prec(n.op)

    def visit_BinOp(self, n):
        if self.prec(n.op) > self.prec(n.left):
            left = r'\left(%s\right)' % self.visit(n.left)
        else:
            left = self.visit(n.left)
        if self.prec(n.op) > self.prec(n.right):
            right = r'\left(%s\right)' % self.visit(n.right)
        else:
            right = self.visit(n.right)
        if isinstance(n.op, ast.Div):
            return r'\frac{%s}{%s}' % (self.visit(n.left), self.visit(n.right))
        elif isinstance(n.op, ast.FloorDiv):
            return r'\left\lfloor\frac{%s}{%s}\right\rfloor' % (self.visit(n.left), self.visit(n.right))
        elif isinstance(n.op, ast.Pow):
            return r'%s^{%s}' % (left, self.visit(n.right))
        else:
            return r'%s %s %s' % (left, self.visit(n.op), right)

    def prec_BinOp(self, n):
        return self.prec(n.op)

    def visit_Sub(self, n):
        return '-'

    def prec_Sub(self, n):
        return 300

    def visit_Add(self, n):
        return '+'

    def prec_Add(self, n):
        return 300

    def visit_Mult(self, n):
        return '\\;'

    def prec_Mult(self, n):
        return 400

    def visit_Mod(self, n):
        return '\\bmod'

    def prec_Mod(self, n):
        return 500

    def prec_Pow(self, n):
        return 700

    def prec_Div(self, n):
        return 400

    def prec_FloorDiv(self, n):
        return 400

    def visit_LShift(self, n):
        return '\\operatorname{shiftLeft}'

    def visit_RShift(self, n):
        return '\\operatorname{shiftRight}'

    def visit_BitOr(self, n):
        return '\\operatorname{or}'

    def visit_BitXor(self, n):
        return '\\operatorname{xor}'

    def visit_BitAnd(self, n):
        return '\\operatorname{and}'

    def visit_Invert(self, n):
        return '\\operatorname{invert}'

    def prec_Invert(self, n):
        return 800

    def visit_Not(self, n):
        return '\\neg'

    def prec_Not(self, n):
        return 800

    def visit_UAdd(self, n):
        return '+'

    def prec_UAdd(self, n):
        return 800

    def visit_USub(self, n):
        return '-'

    def prec_USub(self, n):
        return 800
    def visit_Num(self, n):
        return str(n.n)

    def prec_Num(self, n):
        return 1000

    def generic_visit(self, n):
        if isinstance(n, ast.AST):
            return r'' % (n.__class__.__name__, ', '.join(map(self.visit, [getattr(n, f) for f in n._fields])))
        else:
            return str(n)

    def generic_prec(self, n):
        return 0

def py2tex(expr):
    pt = ast.parse(expr)
    return LatexVisitor().visit(pt.body[0].value)

print(latexSolver("y'=y''-y"))

# print(py2tex("x=2**3"))
# print(py2tex("2*x+constant"))
# print(latexSolver("derivative of 2x^(3xlogx)"))
# print(latexSolver("y'=y''-y"))
# print(py2tex(latexSolver("6 = 3x")))
# print(latex(sympify("y'=y''-y")))
# print(p2t(latexSolver("y'=y''-y")))

# UNCOMMENT OUT THE FOLLOWING LINE IF SYMPY/LATEX IS INSTALLED PROPERLY
# preview(r'$$\\int_0^1 e^x\\,dx$$', viewer='file', filename='test.png', euler=False)