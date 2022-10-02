// window.MathJax = {
//   jax: ["input/TeX", "output/SVG"],
//   extensions: ["tex2jax.js", "MathMenu.js", "MathZoom.js"],
//   showMathMenu: false,
//   showProcessingMessages: false,
//   messageStyle: "none",
//   SVG: {
//     useGlobalCache: false
//   },
//   TeX: {
//     extensions: ["AMSmath.js", "AMSsymbols.js", "autoload-all.js"]
//   },
//   AuthorInit: function() {
//     MathJax.Hub.Register.StartupHook("End", function() {
//       var mj2img = function(texstring, callback) {
//         var input = texstring;
//         var wrapper = document.createElement("div");
//         wrapper.innerHTML = input;
//         var output = { svg: "", img: ""};
//         MathJax.Hub.Queue(["Typeset", MathJax.Hub, wrapper]);
//         MathJax.Hub.Queue(function() {
//           var mjOut = wrapper.getElementsByTagName("svg")[0];
//           mjOut.setAttribute("xmlns", "http://www.w3.org/2000/svg");
//           output.svg = mjOut.outerHTML;
//           var image = new Image();
//           image.src = 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(output.svg)));
//           image.onload = function() {
//             var canvas = document.createElement('canvas');
//             canvas.width = image.width;
//             canvas.height = image.height;
//             var context = canvas.getContext('2d');
//             context.drawImage(image, 0, 0);
//             output.img = canvas.toDataURL('image/png');
//             callback(output);
//           };
//         });
//       }
//       mj2img("\\[f: X \\to Y\\]", function(output){
//         document.getElementById("target").innerText = output.img + '\n' + output.svg;
//       });
//     });
//   }
// };

// (function(d, script) {
//   script = d.createElement('script');
//   script.type = 'text/javascript';
//   script.async = true;
//   script.onload = function() {
//     // remote script has loaded
//   };
//   script.src = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js';
//   d.getElementsByTagName('head')[0].appendChild(script);
// }(document));

// <div id="target"></div>

// const Mathml2latex = require('mathml-to-latex');

// const mathml = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mo>-</mo><mi>b</mi><mo>±</mo><msqrt><mrow><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></mrow></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></mrow></math>';

// Mathml2latex.convert(mathml);
// console.log(mathml)