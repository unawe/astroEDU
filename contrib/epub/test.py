# -*- coding: utf-8 -*-

import epub

def read_file(url):
	import urllib2
	f = urllib2.urlopen(url)
	result = f.read()
	f.close()
	return result

if __name__ == '__main__':
	doc = epub.Document('tada.epub')
	cover = read_file('http://www.unawe.org/static/designimages/logo.png')
	doc.files = [
		('a.xhtml', u'''
<html>
<head>
	<title>Model of a Black Hole</title>
<style>
.title { display: block; font-weight: bold; margin-top: 1em; }
/* 
td { vertical-align:top; }
td+td { width: 200px; }
*/
.box { border: solid 1px black; }
#main { float: left; border: solid 1px red; }
#sidebar { float: right; border: dashed 1px black; width: 200px;  padding: 1em; padding-top: 0; }



#sidebar {
 float:right;
 width:200px;
}
#content {
}
#footer {
}


</style>
</head>

<body>


<div id="title">
	<h1>Model of a Black Hole</h1>
</div>

<div id="sidebar">

	<span class="title">Keywords</span>
	black hole, gravity

	<span class="title">Age Suggestion</span>
	
	 6-7 <br/>
	 8-10 

	
	<span class="title">Time</span>
	?
	

	<span class="title">Cost of materials</span>
	5 €

	
	<span class="title">Individuals / Groups</span>
	
	 Individual 
	

	

	

	

</div>




<div id="content">

	<p>This is an experimental activity that shows how is a black hole doing in the space deforming the space.</p>

	<span class="title">Learning Outcomes</span>
	<p>To build a physical model of the space curvature around a mass and a passing object close to it. To demonstrate what happens to that object if the velocity is not high enough, or if the &quot;well&quot; is deep enough.</p>

	<span class="title">Description</span>
	<ul>

<li>For this experience you will need a piece of a very elastic, stretchy fabric or bandage. If you can, look for the bandage sold in chemists that is used for muscular injuries (Tubifix). You can find these in different sizes, but we are interested in the biggest ones, those which are used for the thorax.</li>

<li>You need to cut ~ 40 cm of the elastic bandage. If it is tubular, you need to cut it through one side, in order to make it flat.</li>

<li>Ask several students to stretch the bandage horizontally until it becomes taut. In this way two dimensional &lsquo;space&rsquo; is represented.</li>

<li>Make a marble (little ball) roll superficially acoss the surface of the bandage: its trajectory should be rectilinear similar to that of a light ray travelling through space.</li>

<li>Place a heavy metal ball on the bandage and you will see how it deforms the fabric of space. &lsquo;Space&rsquo; becomes curved around the heavy mass.</li>

<li>Make the same little marble roll close to the mass. Its trajectory should be deflected by the deformation on the bandage. This is similar to what happens to the light passing close to a massive object which deforms the space surrounding it.</li>

<li>If the mass is really concentrated, ( that is, if the Bocce ball is really heavy) the curvature of the bandage would increase, producing a kind of "gravitational well", from which a marble would not be able to escape.</li>

<li>As the ball passes close by, it starts to revolve around the black hole and eventually it will fall into it. Once in there you can see that things may fall into a black hole but it is difficult for them to come out. This is what happens with black holes: their gravity deforms the space in such a way that the light or any other object can not escape from it.</li>

</ul>
	<div class="clear"></div>

	

	<span class="title">Science Background Information</span>
	<p>A black hole is a region of spacetime whose gravitational field is so strong that nothing which enters it, not even light, can escape.[1] The theory of general relativity predicts that a sufficiently compact mass will deform spacetime to form a black hole. Around a black hole there is a mathematically defined surface called an event horizon that marks the point of no return. It is called ""black"" because it absorbs all the light that hits the horizon, reflecting nothing, just like a perfect black body in thermodynamics.[2][3] Quantum mechanics predicts that black holes emit radiation like a black body with a finite temperature. This temperature is inversely proportional to the mass of the black hole, making it difficult to observe this radiation for black holes of stellar mass or greater.</p>

<p>Objects whose gravity field is too strong for light to escape were first considered in the 18th century by John Michell and Pierre-Simon Laplace. The first modern solution of general relativity that would characterize a black hole was found by Karl Schwarzschild in 1916, although its interpretation as a region of space from which nothing can escape was not fully appreciated for another four decades. Long considered a mathematical curiosity, it was during the 1960s that theoretical work showed black holes were a generic prediction of general relativity. The discovery of neutron stars sparked interest in gravitationally collapsed compact objects as a possible astrophysical reality.</p>

<p>Black holes of stellar mass are expected to form when a star of more than 5 solar masses runs out of energy fuel. This results in the outer layers of gas being thrown out in a supernova explosion. The core of the star collapses and becomes super dense where even the atomic nuclei are squeezed together.The energy density at the core goes to infinity. After a black hole has formed it can continue to grow by absorbing mass from its surroundings. By absorbing other stars and merging with other black holes, supermassive black holes of millions of solar masses may form. There is general consensus that supermassive black holes exist in the centers of most galaxies. In particular, there is strong evidence of a black hole of more than 4 million solar masses at the center of our galaxy, the Milky Way.</p>

<p>Despite its invisible interior, the presence of a black hole can be inferred through its interaction with other matter and with light and other electromagnetic radiation. From stellar movement, the mass and location of an invisible companion object can be calculated. A half-dozen or so binary star systems have been discovered by Astronomers where one of the stars is invisible, yet must surely exist since it pulls with enough gravitational force on the other visible star to make it orbit around their common center of gravity. Therefore these invisible stars are thought to be good candidate black holes. Astronomers have identified numerous stellar black hole candidates in binary systems by studying the movement of their companion stars in this way.</p>
	<div class="clear"></div>

	




	

	


</div>

<div id="footer"><!--<p>copyright statement</p>--></div>




</body>
</html>
<style>#pagewarn { position: absolute; right: 20px; top: 10px; padding-top: 10px; width: 100px; height: 40px; font-weight: bold; text-align: center; color: #000000; background-color: #f4a419; }</style><div id="pagewarn" class="yellow">LOCAL ENVIRONMENT</div>'''), 
		('images/cover.jpg', cover),
	]
	doc.metadata = {
		"title": "TITLE",
		"author": "AUTHOR",
		"book_id": "http://www.unawe.org/activity/actXXX",
		"book_id_type": "URI",
		"language": "en"
	}
	
	doc.compile()