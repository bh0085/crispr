/* http://keith-wood.name/svg.html
   SVG plotting extension for jQuery v1.4.5.
   Written by Keith Wood (kbwood{at}iinet.com.au) December 2008.
   Dual licensed under the GPL (http://dev.jquery.com/browser/trunk/jquery/GPL-LICENSE.txt) and
   MIT (http://dev.jquery.com/browser/trunk/jquery/MIT-LICENSE.txt) licenses.
   Please attribute the author if you use it. */
eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('(r($){$.1S.2r(\'2a\',1T);r 1T(a){4.u=a;4.1i=1j;4.M={11:\'\',1k:25,1z:{1l:\'1A\'}};4.12=[0.1,0.1,0.8,0.9];4.1B={17:\'2b\',U:\'1U\'};4.Q=[];4.1C=18;4.13=[];4.1D=z;4.1V=1m 2s().2t();4.t=4.u.1S(0,0,0,0,{19:\'1S-2a\'});4.G=1m 1E(4);4.G.1n(\'X\',20);4.N=1m 1E(4);4.N.1n(\'Y\',20);4.P=1m 1W(4);4.1i=18}$.K(1T.1F,{X:0,Y:1,W:2,H:3,L:0,T:1,R:2,B:3,2u:r(a){7(E.D==0){q 4.t}4.t=a;q 4},2c:r(a,b,c,d){7(E.D==0){q 4.12}4.12=(1G(a)?a:[a,b,c,d]);4.F();q 4},1H:r(a,b,c){7(E.D==0){q 4.1B}7(I b==\'2d\'){c=b;b=z}4.1B=$.K({17:a},(b?{U:b}:{}),c||{});4.F();q 4},2v:r(a,b){7(E.D==0){q 4.Q}4.Q=[(I a==\'14\'?{U:a}:a),(I b==\'14\'?{U:b}:b)];7(4.Q[0]==z&&4.Q[1]==z){4.Q=[]}4.F();q 4},2w:r(a){7(E.D==0){q 4.1C}4.1C=a;q 4},1n:r(a,b,c,d){7(E.D==0){q 4.M}7(I b!=\'1e\'){d=c;c=b;b=z}7(I c!=\'14\'){d=c;c=z}4.M={11:a,1k:b||4.M.1k,1z:$.K({1l:\'1A\'},(c?{17:c}:{}),d||{})};4.F();q 4},2x:r(a,b,c,d,e,f,g){4.13.2y(1m 1X(4,a,b,c,d,e,f,g));4.F();q 4},2z:r(i){q(E.D>0?4.13[i]:z)||4.13},2A:r(){4.1i=1j;q 4},2B:r(){4.1i=18;4.F();q 4},2C:r(a){4.1D=a;q 4},F:r(){7(!4.1i){q}1Y(4.t.2e){4.t.2D(4.t.2e)}7(!4.t.2E){4.u.2F.2G(4.t)}7(!4.t.S){4.t.2f(\'S\',1Z(4.t.21(\'S\'),10)||4.u.22())}1o 7(4.t.S.16){4.t.S.16.11=4.t.S.16.11||4.u.22()}1o{4.t.S=4.t.S||4.u.22()}7(!4.t.V){4.t.2f(\'V\',1Z(4.t.21(\'V\'),10)||4.u.23())}1o 7(4.t.V.16){4.t.V.16.11=4.t.V.16.11||4.u.23()}1o{4.t.V=4.t.V||4.u.23()}4.2g();6 a=4.1a();6 b=4.u.2H(4.t,\'2h\',{2I:\'2i\'+4.1V});4.u.1I(b,a[4.X],a[4.Y],a[4.W],a[4.H]);4.A=4.u.1f(4.t,{19:\'2J\',2h:\'2K(#2i\'+4.1V+\')\'});4.24(18);4.24(1j);26(6 i=0;i<4.13.D;i++){4.2j(4.13[i],i)}4.2k();4.2l()},1J:r(a,b){q(!a[b]?1Z(a.21(b),10):(a[b].16?a[b].16.11:a[b]))},1a:r(a){6 b=(a!=z);a=a||4.12;6 c=4.1J(4.t,\'S\');6 d=4.1J(4.t,\'V\');6 e=(a[4.L]>1?a[4.L]:c*a[4.L]);6 f=(a[4.T]>1?a[4.T]:d*a[4.T]);6 g=(a[4.R]>1?a[4.R]:c*a[4.R])-e;6 h=(a[4.B]>1?a[4.B]:d*a[4.B])-f;7(4.1C&&!b){6 i=1p.C(g/(4.G.s.J-4.G.s.C),h/(4.N.s.J-4.N.s.C));g=i*(4.G.s.J-4.G.s.C);h=i*(4.N.s.J-4.N.s.C)}q[e,f,g,h]},1K:r(){6 a=4.1a();q[a[4.W]/(4.G.s.J-4.G.s.C),a[4.H]/(4.N.s.J-4.N.s.C)]},2g:r(a,b){6 c=4.u.1f(4.t,{19:\'2L\'});6 d=4.1a();4.u.1I(c,d[4.X],d[4.Y],d[4.W],d[4.H],4.1B);7(4.Q[0]&&4.N.w.O&&!b){4.27(c,18,4.Q[0],d)}7(4.Q[1]&&4.G.w.O&&!a){4.27(c,1j,4.Q[1],d)}q c},27:r(a,b,c,d){6 g=4.u.1f(a,c);6 e=(b?4.N:4.G);6 f=4.1K();6 h=1p.28(e.s.C/e.w.O)*e.w.O;h+=(h<=e.s.C?e.w.O:0);1Y(h<e.s.J){6 v=(b?e.s.J-h:h-e.s.C)*f[b?1:0]+(b?d[4.Y]:d[4.X]);4.u.1q(g,(b?d[4.X]:v),(b?v:d[4.Y]),(b?d[4.X]+d[4.W]:v),(b?v:d[4.Y]+d[4.H]));h+=e.w.O}},24:r(a){6 b=(a?\'x\':\'y\')+\'2M\';6 c=(a?4.G:4.N);6 d=(a?4.N:4.G);6 e=4.1a();6 f=4.1K();6 g=4.u.1f(4.A,$.K({19:b},c.1r));6 h=4.u.1f(4.A,$.K({19:b+\'2N\',1l:(a?\'1A\':\'1s\')},c.1L));6 i=(a?d.s.J:-d.s.C)*f[a?1:0]+(a?e[4.Y]:e[4.X]);4.u.1q(g,(a?e[4.X]:i),(a?i:e[4.Y]),(a?e[4.X]+e[4.W]:i),(a?i:e[4.Y]+e[4.H]));7(c.w.O){6 j=c.w.1M;6 k=1p.28(c.s.C/c.w.O)*c.w.O;k=(k<c.s.C?k+c.w.O:k);6 l=(!c.w.1b?c.s.J+1:1p.28(c.s.C/c.w.1b)*c.w.1b);l=(l<c.s.C?l+c.w.1b:l);6 m=[(c.w.1c==\'2O\'||c.w.1c==\'29\'?-1:0),(c.w.1c==\'2P\'||c.w.1c==\'29\'?+1:0)];1Y(k<=c.s.J||l<=c.s.J){6 n=1p.C(k,l);6 o=(n==k?j:j/2);6 p=(a?n-c.s.C:c.s.J-n)*f[a?0:1]+(a?e[4.X]:e[4.Y]);4.u.1q(g,(a?p:i+o*m[0]),(a?i+o*m[0]:p),(a?p:i+o*m[1]),(a?i+o*m[1]:p));7(n==k&&n!=0){4.u.1t(h,(a?p:i-j),(a?i-j:p),\'\'+n)}k+=(n==k?c.w.O:0);l+=(n==l?c.w.1b:0)}}7(c.M){7(a){4.u.1t(4.t,e[4.X]-c.1g,i,c.M,$.K({1l:\'1s\'},c.1u||{}))}1o{4.u.1t(4.t,i,e[4.Y]+e[4.H]+c.1g,c.M,$.K({1l:\'1A\'},c.1u||{}))}}},2j:r(a,b){6 c=4.1a();6 d=4.1K();6 e=4.u.2Q();6 f=a.1N||[4.G.s.C,4.G.s.J];6 g=(f[1]-f[0])/a.1v;6 h=18;26(6 i=0;i<=a.1v;i++){6 x=f[0]+i*g;7(x>4.G.s.J+g){2R}7(x<4.G.s.C-g){2S}6 j=(x-4.G.s.C)*d[0]+c[4.X];6 k=c[4.H]-((a.1O(x)-4.N.s.C)*d[1])+c[4.Y];e[(h?\'2T\':\'1q\')+\'2U\'](j,k);h=1j}6 p=4.u.2V(4.A,e,$.K({19:\'2m\'+b,17:\'2b\',U:a.1h,1w:a.1x},a.1P||{}));4.2n(p,a.1d)},2k:r(){4.u.1t(4.t,4.1J(4.t,\'S\')/2,4.M.1k,4.M.11,4.M.1z)},2l:r(){7(!4.P.1Q){q}6 g=4.u.1f(4.t,{19:\'P\'});6 a=4.1a(4.P.12);4.u.1I(g,a[4.X],a[4.Y],a[4.W],a[4.H],4.P.1R);6 b=a[4.W]>a[4.H];6 c=4.13.D;6 d=(b?a[4.W]:a[4.H])/c;6 e=a[4.X]+5;6 f=a[4.Y]+((b?a[4.H]:d)+4.P.Z)/2;26(6 i=0;i<c;i++){6 h=4.13[i];4.u.1I(g,e+(b?i*d:0),f+(b?0:i*d)-4.P.Z,4.P.Z,4.P.Z,{17:h.1h});4.u.1t(g,e+(b?i*d:0)+4.P.Z+5,f+(b?0:i*d),h.1d,4.P.1y)}},2n:r(b,c){6 d=4.1D;7(4.1D){$(b).2W(r(a){d.2o(4,[c])},r(){d.2o(4,[\'\'])})}}});r 1X(a,b,c,d,e,f,g,h){7(I b!=\'14\'){h=g;g=f;f=e;e=d;d=c;c=b;b=z}7(!1G(d)){h=g;g=f;f=e;e=d;d=z}7(I e!=\'1e\'){h=g;g=f;f=e;e=z}7(I f!=\'14\'){h=g;g=f;f=z}7(I g!=\'1e\'){h=g;g=z}4.A=a;4.1d=b||\'\';4.1O=c||2p;4.1N=d;4.1v=e||2q;4.1h=f||\'1U\';4.1x=g||1;4.1P=h||{}}$.K(1X.1F,{2X:r(a){7(E.D==0){q 4.1d}4.1d=a;4.A.F();q 4},2m:r(a,b){7(E.D==0){q 4.1O}7(I a==\'r\'){b=a;a=z}4.1d=a||4.1d;4.1O=b;4.A.F();q 4},2Y:r(a,b){7(E.D==0){q 4.1N}4.1N=(a==z?z:[a,b]);4.A.F();q 4},2Z:r(a){7(E.D==0){q 4.1v}4.1v=a;4.A.F();q 4},1H:r(a,b,c){7(E.D==0){q $.K({U:4.1h,1w:4.1x},4.1P)}7(I b!=\'1e\'){c=b;b=z}4.1h=a||4.1h;4.1x=b||4.1x;$.K(4.1P,c||{});4.A.F();q 4},1s:r(){q 4.A}});r 2p(x){q x}r 1E(a,b,c,d,e,f){4.A=a;4.M=b||\'\';4.1u={};4.1g=0;4.1L={};4.1r={U:\'1U\',1w:1};4.w={O:e||10,1b:f||0,1M:10,1c:\'29\'};4.s={C:c||0,J:d||2q};4.30=0}$.K(1E.1F,{31:r(a,b){7(E.D==0){q 4.s}4.s.C=a;4.s.J=b;4.A.F();q 4},32:r(a,b,c,d){7(E.D==0){q 4.w}7(I c==\'14\'){d=c;c=z}4.w.O=a;4.w.1b=b;4.w.1M=c||4.w.1M;4.w.1c=d||4.w.1c;4.A.F();q 4},1n:r(a,b,c,d){7(E.D==0){q{1n:4.M,1k:4.1g,1H:4.1u}}7(I b!=\'1e\'){d=c;c=b;b=z}7(I c!=\'14\'){d=c;c=z}4.M=a;4.1g=(b!=z?b:4.1g);7(c||d){4.1u=$.K(d||{},(c?{17:c}:{}))}4.A.F();q 4},1H:r(a,b){7(E.D==0){q 4.1L}7(I a!=\'14\'){b=a;a=z}4.1L=$.K(b||{},(a?{17:a}:{}));4.A.F();q 4},1q:r(a,b,c){7(E.D==0){q 4.1r}7(I b!=\'1e\'){c=b;b=z}$.K(4.1r,{U:a,1w:b||4.1r.1w},c||{});4.A.F();q 4},1s:r(){q 4.A}});r 1W(a,b,c){4.A=a;4.1Q=18;4.12=[0.9,0.1,1.0,0.9];4.Z=15;4.1R=b||{U:\'33\'};4.1y=c||{}}$.K(1W.1F,{34:r(a){7(E.D==0){q 4.1Q}4.1Q=a;4.A.F();q 4},2c:r(a,b,c,d){7(E.D==0){q 4.12}4.12=(1G(a)?a:[a,b,c,d]);4.A.F();q 4},1z:r(a,b,c){7(E.D==0){q{35:4.Z,36:4.1R,37:4.1y}}7(I a==\'2d\'){c=b;b=a;a=z}4.Z=a||4.Z;4.1R=b;4.1y=c||4.1y;4.A.F();q 4},1s:r(){q 4.A}});r 1G(a){q(a&&a.38==39)}})(3a)',62,197,'||||this||var|if|||||||||||||||||||return|function|_scale|_plotCont|_wrapper||_ticks|||null|_plot||min|length|arguments|_drawPlot|xAxis||typeof|max|extend||_title|yAxis|major|legend|_gridlines||width||stroke|height||||_sampleSize||value|_area|_functions|string||baseVal|fill|true|class_|_getDims|minor|position|_name|number|group|_titleOffset|_stroke|_drawNow|false|offset|textAnchor|new|title|else|Math|line|_lineFormat|end|text|_titleFormat|_points|strokeWidth|_strokeWidth|_textSettings|settings|middle|_areaFormat|_equalXY|_onstatus|SVGPlotAxis|prototype|isArray|format|rect|_getValue|_getScales|_labelFormat|size|_range|_fn|_settings|_show|_bgSettings|svg|SVGPlot|black|_uuid|SVGPlotLegend|SVGPlotFunction|while|parseInt||getAttribute|_width|_height|_drawAxis||for|_drawGridlines|floor|both|plot|none|area|object|firstChild|setAttribute|_drawChartBackground|clipPath|clip|_plotFunction|_drawTitle|_drawLegend|fn|_showStatus|apply|identity|100|addExtension|Date|getTime|container|gridlines|equalXY|addFunction|push|functions|noDraw|redraw|status|removeChild|parent|_svg|appendChild|other|id|foreground|url|background|Axis|Labels|nw|se|createPath|break|continue|move|To|path|hover|name|range|points|_crossAt|scale|ticks|gray|show|sampleSize|bgSettings|textSettings|constructor|Array|jQuery'.split('|'),0,{}))
