<html>
<head>
    <!-- author: Rainer Hoerbe -->
    <title> SAML Echo Service </title>
    <link type="text/css" rel="stylesheet" media="all" href="default.css" />
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" ></script>
    <!-- To obtain the status page it must be access with the valid session cookie. 
         php/SSI etc. will not work therefore. A client-side include using jQuery is used instead. 
         Its contents is transferred to a <div> to allow for variable height.
    -->
    <!--script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js"></script-->
    
    <link rel="stylesheet" href="http://yandex.st/highlightjs/8.0/styles/default.min.css">

    <link rel="stylesheet" href="styles/default.css">

    <script>
        function loadXMLDoc() {
        
            // configure SP to export the Assertion: https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPAssertionExport
            /*var xmlhttp1;
            xmlhttp1=new XMLHttpRequest();
            xmlhttp1.onreadystatechange=function() {
              if (xmlhttp1.readyState==4 && xmlhttp1.status==200) {
                document.getElementById("SAMLAssertion").innerHTML=xmlhttp1.responseText;
              }
            }
            xmlhttp1.open("POST","/cgi-bin/prettyxml.cgi", true);
            xmlhttp1.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xmlhttp1.send('xmlurl=<?php echo urlencode($_SERVER["Shib-Assertion-01"]); ?>');
            */
            
            var xmlhttp2;
            xmlhttp2=new XMLHttpRequest();

            xmlhttp2.onreadystatechange=function() {
              if (xmlhttp2.readyState==4 && xmlhttp2.status==200) {
                document.getElementById("ShibStatus").innerHTML=xmlhttp2.responseText;
              }
            }
            xmlhttp2.open("GET","/Shibboleth.sso/Session", true);
            xmlhttp2.send();
        }
    </script>

</head>

<body onload="loadXMLDoc()">

<h1>Echo Service showing SAML response</h1>
<p style="text-align: right; font-size: 1.2em"><a href="/Shibboleth.sso/Logout?return=/index.html">Logout</a></p>
<h2>Shibboleth Session Info</h2>
<p>Client Address is not correct but that of the proxy (apache httpd problem with XFF)</p>
<div id="ShibStatus"></div>

<hr>

<h2>SAML Assertion Contents</h2>

<table style="margin-top: 2em">
    <colgroup> <col width="300"> <col width="800"> <col width=" 320"> </colgroup>
    <caption style="color: red">Request Information</caption>
    <tr><th style="width=13em">Name</th><th>Wert</th>
    <tr><td>HTTP_HOST</td><td><?php echo $_SERVER["HTTP_HOST"]; ?></td>
    </tr><tr><td>REQUEST_URI           </td><td><?php echo $_SERVER["REQUEST_URI"]; ?></td>
    </tr>
</table>

<table style="margin-top: 2em">
    <colgroup> <col width="300"> <col width="800"> <col width=" 320"> </colgroup>
    <caption style="color: red">Edushare Full Attribute Set (Test)</caption>
    <tr><th style="width=13em">Name</th><th>Wert</th>
    </tr><tr><td colspan="2" style="padding-left: 13em"></td>
    </tr><tr><td <?php echo $_SERVER["gender"] ? 'style="color:black"' : ""; ?>>gender</td><td><?php echo $_SERVER["gender"]; ?></td> 
    </tr><tr><td <?php echo $_SERVER["givenName"] ? 'style="color:black"' : ""; ?>>givenName       </td><td><?php echo $_SERVER["givenName"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["surname"] ? 'style="color:black"' : ""; ?>>surname          </td><td><?php echo $_SERVER["surname"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["cn"] ? 'style="color:black"' : ""; ?>>cn</td><td><?php echo $_SERVER["cn"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["uid"] ? 'style="color:black"' : ""; ?>>uid             </td><td><?php echo $_SERVER["uid"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["mail"] ? 'style="color:black"' : ""; ?>>mail             </td><td><?php echo $_SERVER["mail"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["rolle"] ? 'style="color:black"' : ""; ?>>Rolle             </td><td><?php echo $_SERVER["rolle"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["skz"] ? 'style="color:black"' : ""; ?>>Schulkennzahl            </td><td><?php echo $_SERVER["skz"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["klasse"] ? 'style="color:black"' : ""; ?>>Klasse            </td><td><?php echo $_SERVER["klasse"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["schulstandort"] ? 'style="color:black"' : ""; ?>>Schulstandort             </td><td><?php echo $_SERVER["schulstandort"]; ?></td>
    </tr>
</table>
<table style="margin-top: 2em">
    <colgroup> <col width="300"> <col width="800"> <col width=" 320"> </colgroup>
    <caption style="color: red">Other SAML Assertion Elements</caption>
    <tr><th style="width=13em">Name</th><th>Wert</th>
    <?php echo $_SERVER["NameID-persistent"] ? '<tr><td style="color:black">saml:NameID (persistent)</td><td>' . $_SERVER["NameID-persistent"] . "</td></tr>" : ""; ?>
    <?php echo $_SERVER["NameID-transient"]  ? '<tr><td style="color:black">saml:NameID (transient)</td><td>' . $_SERVER["NameID-transient"] . "</td></tr>" : ""; ?>
    <?php echo $_SERVER["NameID-unspec"] ? '<tr><td style="color:black">saml:NameID (unspecified)</td><td>' . $_SERVER["NameID-unspec"] . "</td></tr>" : ""; ?>
    <tr><td <?php echo $_SERVER["Shib-AuthnContext-Class"] ? 'style="color:black"' : ""; ?>>saml:AuthnContextClass</td><td><?php echo $_SERVER["Shib-AuthnContext-Class"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["Shib-Session-ID"] ? 'style="color:black"' : ""; ?>>Shib Session-ID</td><td><?php echo $_SERVER["Shib-Session-ID"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["Shib-Identity-Provider"] ? 'style="color:black"' : ""; ?>>saml:Issuer</td><td><?php echo $_SERVER["Shib-Identity-Provider"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["Shib-Authentication-Instant"] ? 'style="color:black"' : ""; ?>>SAML Authentication Instant</td><td><?php echo $_SERVER["Shib-Authentication-Instant"]; ?></td>
    </tr><tr><td <?php echo $_SERVER["Shib-Session-Index"] ? 'style="color:black"' : ""; ?>>saml:SessionIndex</td><td><?php echo $_SERVER["Shib-Session-Index"]; ?></td>
    </tr>
</table>

<hr>

<!--
<h2>SAML Assertion 1</h2>
  <div>
    <pre class="prettyprint linenums">
      <p id="SAMLAssertion">
      <?php echo $_SERVER["Shib-Assertion-01"]; ?>
      </p>
    </pre>
  </div>

<hr>
-->

<!--
<h2>PHP $_SERVER var</h2>
      <?php var_dump($_SERVER) ?>
-->
<!--
<h1>SP Metadata</h1>
<div id="XMLHolder"> </div>
<LINK href="XMLDisplay.css" type="text/css" rel="stylesheet">
<script type="text/javascript" src="XMLDisplay.js"> </script>
<script>LoadXML('XMLHolder','https://sp2.test.wpv.portalverbund.at/sp.xml'); </script>
<script src="http://yandex.st/highlightjs/8.0/highlight.min.js"></script>
-->

</body>
</html>
