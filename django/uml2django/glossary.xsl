<?xml version="1.0" encoding="UTF-8"?>
<!--
UML to Django

@author: geoffroy.noel@kcl.ac.uk
@doc: http://confluence.cch.kcl.ac.uk//x/1QAq
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
								xmlns:ArgoUML="org.omg.xmi.namespace.UML"
								xmlns:StarUML="href://org.omg/UML/1.3"
								xmlns:UML="org.omg.xmi.namespace.UML"
								xmlns:fn="http://www.w3.org/2005/xpath-functions"
								xmlns:xmidj="xmi2dj"
								>

<xsl:import href="xmilib.xsl"/>

<xsl:output method="xml" omit-xml-declaration="yes" indent="yes" />

<xsl:key name="datatypes" match="//UML:DataType[@xmi.id]" use="@xmi.id" />
<xsl:key name="classes" match="//UML:Class[@xmi.id]" use="@xmi.id" />
<xsl:key name="stereotypes" match="//UML:Stereotype[@xmi.id]" use="@xmi.id" />
<xsl:key name="tags" match="//UML:TagDefinition[@xmi.id]" use="@xmi.id" />
<!-- xsl:key name="associationEnd" match="//UML:AssociationEnd.participant/UML:Class" use="@xmi.idref" / -->

<!-- ========================== -->
<!-- 		ROOT TEMPLATE 		-->
<!-- ========================== -->

<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style>
table {
	border: 1px solid black;
	margin: 10px 5px 5px 5px;
	width: 680px;
}
thead tr {
	background-color: green;
	color: white;
	font-weight: bolder;
	text-align: center;
}
table tr td {
	border-bottom: 1px solid lightgrey;
}
#uml-toc {
	width: 200px;
	float: left;
}
#uml-tables {
	width: 200px;
	float: left;
}
.anchor a {
color: lightgrey;
}
.anchor {
float:left;
font-weight: normal;
}


</style>
</head>
<body>
		
<!-- xsl:apply-templates select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement/UML:Package/UML:Namespace.ownedElement/UML:Class[@name and @name != '' and substring(@name,1,1) != '_']"/ -->
<!-- Make sure we declare the base classes first otherwise Python will not compile our code -->
<!-- note that the following method doesn't work multiple level of inheritence -->
<div id="uml-toc">
<ul>
<xsl:for-each select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement/UML:Package/UML:Namespace.ownedElement/UML:Class[@xmi.id]">
	<xsl:sort select="@name"/>
	<xsl:if test="count(//UML:Generalization.parent/UML:Class[@xmi.idref = current()/@xmi.id]) > 0">
	<li>
		<xsl:variable name="classid" select="@xmi.id" />
		<a href="#{$classid}"><xsl:value-of select="@name"/></a>
	</li>
	</xsl:if>
</xsl:for-each>
<xsl:for-each select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement/UML:Package/UML:Namespace.ownedElement/UML:Class[@xmi.id]">
	<xsl:sort select="@name"/>
	<xsl:if test="count(//UML:Generalization.parent/UML:Class[@xmi.idref = current()/@xmi.id]) = 0">
	<li>
		<xsl:variable name="classid" select="@xmi.id" />
		<a href="#{$classid}"><xsl:value-of select="@name"/></a>
	</li>
	</xsl:if>
</xsl:for-each>
</ul>
</div>

<a name="uml-top"></a>

<div id="uml-tables">
<xsl:for-each select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement/UML:Package/UML:Namespace.ownedElement/UML:Class[@xmi.id]">
	<xsl:sort select="@name"/>
	<xsl:if test="count(//UML:Generalization.parent/UML:Class[@xmi.idref = current()/@xmi.id]) > 0">
		<xsl:apply-templates select="." />
	</xsl:if>
</xsl:for-each>
<xsl:for-each select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement/UML:Package/UML:Namespace.ownedElement/UML:Class[@xmi.id]">
	<xsl:sort select="@name"/>
	<xsl:if test="count(//UML:Generalization.parent/UML:Class[@xmi.idref = current()/@xmi.id]) = 0">
		<xsl:apply-templates select="." />
	</xsl:if>
</xsl:for-each>
<!-- # Many To Many Tables --> 
<!-- xsl:apply-templates select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:Association/UML:Association.connection"/ -->
<!-- xsl:apply-templates select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:AssociationClass/UML:Association.connection"/ -->
</div>

</body>
</html>
</xsl:template>

<!-- ========================== -->
<!-- 		CLASS TEMPLATE 		-->
<!-- ========================== -->

<xsl:template match="UML:Class">
<xsl:variable name="classid" select="@xmi.id" />
<table>
	<thead>
		<tr>
			<td colspan="2">
				<span class="anchor"><a href="#uml-top">top</a></span>
				<a name="{$classid}"><xsl:value-of select="@name"/></a>
			</td>
		</tr>
	</thead>

<xsl:apply-templates select="UML:Classifier.feature/UML:Attribute" />

<xsl:call-template name="ConvertClassAssociations"><xsl:with-param name="classid" select="@xmi.id"/></xsl:call-template>

</table>

</xsl:template>

<!-- ========================== -->
<!-- 		FK TEMPLATE 		-->
<!-- ========================== -->

<xsl:template name="ConvertClassAssociations">
<!-- Converts 1-n or n-n associations into ForeignKey fields in the class -->
<!-- [classid] if the xmi.id of the class we are currently converting into django -->
<xsl:param name="classid" />
<!-- find all the end of all the 1-n or n-n associations, the end point to this class -->
<xsl:for-each select="//UML:Association/UML:Association.connection/UML:AssociationEnd[descendant::UML:MultiplicityRange/@upper = '-1'][UML:AssociationEnd.participant/UML:Class/@xmi.idref = $classid]
						| //UML:AssociationClass[UML:Association.connection/UML:AssociationEnd[descendant::UML:MultiplicityRange/@upper = '-1']/UML:AssociationEnd.participant/UML:Class/@xmi.idref = $classid]">
	<!-- name of the ending to this class -->
	<xsl:variable name="endName" select="@name" />
	<!-- Find the class at other end -->
	<!-- xsl:for-each select="descendant::UML:AssociationEnd.participant/UML:Class[@xmi.idref != $classid]" -->
	<xsl:for-each select="../UML:AssociationEnd[@xmi.id != current()/@xmi.id]" >
		<xsl:variable name="otherClassid" select="UML:AssociationEnd.participant/UML:Class/@xmi.idref" />
		<!-- Continue if that end is 1 
			OR 
			it is the first end (a way to choose an arbitrary model where we declare the many2many key) -->
		<xsl:if test="(descendant::UML:MultiplicityRange/@upper = '1') or ($otherClassid = ../UML:AssociationEnd[1]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)">
		<tr><td>
		<!-- todo: foreign key name should be the name of an end of the association, if absent then we must use the name of the foreign table -->
		<!-- todo: the association name should be used for the joint table -->
		<!-- xsl:value-of select="xmidj:getDjIdentifierL(@name)" / -->
		<xsl:choose>
			<!-- if 1-n AND there is a name for that end of the connection then use it -->
			<!-- xsl:when test="$endName != '' and descendant::UML:MultiplicityRange/@upper = '1'" -->
			<xsl:when test="$endName != ''">
				<xsl:value-of select="name" select="$endName"/>
			</xsl:when>
			<!-- Otherwise just use the other class name -->
			<xsl:otherwise>
				<xsl:value-of select="name" select="key('classes', $otherClassid)/@name"/>
			</xsl:otherwise>
		</xsl:choose> 
		<xsl:choose>
			<xsl:when test="descendant::UML:MultiplicityRange/@upper = '1'"><br/>(-&gt; </xsl:when>
			<xsl:otherwise><br/>(&lt;=&gt; </xsl:otherwise>
		</xsl:choose>
			<!-- self reference? -->
		<xsl:choose>
			<xsl:when test="$classid = $otherClassid">self</xsl:when>
			<xsl:otherwise><xsl:value-of select="key('classes', $otherClassid)/@name"/></xsl:otherwise>
		</xsl:choose>
		<xsl:text>)</xsl:text>
		<!-- xsl:choose>
	 		<xsl:when test="@name != ''">
	 			<xsl:text>related_name='</xsl:text>
	 			<xsl:call-template name="getDjIdentifier"><xsl:with-param name="name" select="@name"/></xsl:call-template>
	 			<xsl:text>', </xsl:text>
	 		</xsl:when>
	 		<xsl:when test="$endName != ''">
	 			<xsl:text>related_name='%(class)s_</xsl:text>
	 			<xsl:call-template name="getDjIdentifier"><xsl:with-param name="name" select="$endName"/></xsl:call-template>
	 			<xsl:text>', </xsl:text>
	 		</xsl:when>
		</xsl:choose -->
		</td><td>
		<xsl:for-each select="../../UML:ModelElement.taggedValue/UML:TaggedValue[UML:TaggedValue.type/UML:TagDefinition/@href = 'http://argouml.org/profiles/uml14/default-uml14.xmi#.:000000000000087C']">
			<xsl:value-of select="UML:TaggedValue.dataValue"/>
		</xsl:for-each>.
		</td></tr>
	 	</xsl:if>
	</xsl:for-each>	
</xsl:for-each>
</xsl:template>

<!-- ========================== -->
<!-- 	ATTRIBUTE TEMPLATE 		-->
<!-- ========================== -->

<xsl:template match="UML:Classifier.feature/UML:Attribute">
<tr>
	<td style="width:200px;">
		<xsl:value-of select="@name"/>
	</td>
	<td>
		<xsl:for-each select="UML:ModelElement.taggedValue/UML:TaggedValue[UML:TaggedValue.type/UML:TagDefinition/@href = 'http://argouml.org/profiles/uml14/default-uml14.xmi#.:000000000000087C']">
			<xsl:call-template name="getShortDoc"><xsl:with-param name="text"><xsl:value-of select="UML:TaggedValue.dataValue"/></xsl:with-param></xsl:call-template>
		</xsl:for-each>.
	</td>
</tr>
</xsl:template>

<!-- ========================== -->
<!-- 	CONNECTION TEMPLATE 	-->
<!-- ========================== -->

<xsl:template match="UML:Association.connection">
<xsl:if test="UML:AssociationEnd[1]//UML:MultiplicityRange/@upper = '-1' and UML:AssociationEnd[2]//UML:MultiplicityRange/@upper = '-1'">
<xsl:text>
#
class </xsl:text>
	<xsl:call-template name="getDjIdentifier"><xsl:with-param name="name" select="key('classes', UML:AssociationEnd[1]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name"/></xsl:call-template>
	<xsl:text>_</xsl:text>
	<xsl:call-template name="getDjIdentifier"><xsl:with-param name="name" select="key('classes', UML:AssociationEnd[2]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name"/></xsl:call-template>
	<xsl:text>(models.Model):
</xsl:text>

	<xsl:for-each select=".//UML:AssociationEnd.participant/UML:Class" >
		<xsl:text><![CDATA[	]]></xsl:text>
		<xsl:call-template name="getDjIdentifierL"><xsl:with-param name="name" select="key('classes', @xmi.idref)/@name"/></xsl:call-template> = models.ForeignKey('<xsl:call-template name="getDjIdentifier"><xsl:with-param name="name" select="key('classes', @xmi.idref)/@name"/></xsl:call-template>
		<xsl:text>')
</xsl:text>
	</xsl:for-each>

<xsl:if test="count(../UML:Classifier.feature/UML:Attribute) > 0" >
	<xsl:text>
	# association fields 
</xsl:text>
	<xsl:apply-templates select="../UML:Classifier.feature/UML:Attribute" />
</xsl:if>

</xsl:if>
</xsl:template>

</xsl:stylesheet>
