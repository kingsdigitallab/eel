<?xml version="1.0" encoding="UTF-8"?>
<!--
UML to Django

@author: geoffroy.noel@kcl.ac.uk
@doc: http://confluence.cch.kcl.ac.uk//x/1QAq
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
								xmlns:UML="org.omg.xmi.namespace.UML"
								xmlns:xmidj="xmi2dj"
								xmlns:fn="http://www.w3.org/2005/xpath-functions">
<xsl:import href="xmilib.xsl"/>

<xsl:output method="text" omit-xml-declaration="yes" indent="no" />

<xsl:key name="classes" match="//UML:Class" use="@xmi.id" />
<xsl:key name="stereotypes" match="//UML:Stereotype[@xmi.id]" use="@xmi.id" />

<!-- ========================== -->
<!-- 		ROOT TEMPLATE 		-->
<!-- ========================== -->

<xsl:template match="/">
<xml:text># Auto generated from an XMI file
# Do not edit this file
# Edit admin_custom.py instead
from models import *
from django.contrib import admin
</xml:text>

<xsl:apply-templates select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:Association/UML:Association.connection"/>
<xsl:apply-templates select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:AssociationClass/UML:Association.connection"/>
<xsl:apply-templates select="//UML:Class[@name and @name != '' and substring(@name,1,1) != '_']"/>
#
</xsl:template>

<!-- ========================== -->
<!-- 		CLASS TEMPLATE 		-->
<!-- ========================== -->

<xsl:template match="//UML:Class">
#
class <xsl:value-of select="translate(@name, ' ', '_')" />Admin(admin.ModelAdmin):
	model = <xsl:value-of select="translate(@name, ' ', '_')" />

	verbose_name = '<xsl:value-of select="@name" />'
	verbose_name_plural = '<xsl:call-template name="getPlural"><xsl:with-param name="class" select="."/></xsl:call-template>'

	inlines = (<xsl:for-each select="/XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:Association/UML:Association.connection[descendant::UML:AssociationEnd.participant/UML:Class/@xmi.idref = current()/@xmi.id]
									| /XMI/XMI.content/UML:Model/UML:Namespace.ownedElement//UML:AssociationClass/UML:Association.connection[descendant::UML:AssociationEnd.participant/UML:Class/@xmi.idref = current()/@xmi.id]">
		<xsl:if test="UML:AssociationEnd[1]//UML:MultiplicityRange/@upper = '-1' and UML:AssociationEnd[2]//UML:MultiplicityRange/@upper = '-1'">
			<xsl:value-of select="translate(key('classes', UML:AssociationEnd[1]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name, ' ', '_')" />
			<xsl:text>_</xsl:text>
			<xsl:value-of select="translate(key('classes', UML:AssociationEnd[2]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name, ' ', '_')" />
			<xsl:text>Inline, </xsl:text>
		</xsl:if>
	</xsl:for-each>)
	
	<!-- List all the fields in the PK -->
	<xsl:if test="UML:Classifier.feature/UML:Attribute/UML:ModelElement.stereotype/UML:Stereotype[key('stereotypes', @xmi.idref)/@name = 'PK']" >
	list_display = (<xsl:for-each select="UML:Classifier.feature/UML:Attribute">
			<xsl:if test="UML:ModelElement.stereotype/UML:Stereotype[key('stereotypes', @xmi.idref)/@name = 'PK']">
				<xsl:text>'</xsl:text><xsl:call-template name="getDjIdentifierL"><xsl:with-param name="name" select="@name"/></xsl:call-template><xsl:text>', </xsl:text>
			</xsl:if>
		</xsl:for-each>)
	</xsl:if> 

	<!-- Search on the first PK field -->
	<!-- TODO: search on first char/string PK field -->
	<xsl:for-each select="UML:Classifier.feature/UML:Attribute[UML:ModelElement.stereotype/UML:Stereotype[key('stereotypes', @xmi.idref)/@name = 'PK']][1]">
		<xsl:text>search_fields = ['</xsl:text><xsl:call-template name="getDjIdentifierL"><xsl:with-param name="name" select="@name"/></xsl:call-template><xsl:text>', ]
</xsl:text>
	</xsl:for-each>

</xsl:template>

<!-- ========================== -->
<!-- 	CONNECTION TEMPLATE 	-->
<!-- ========================== -->

<xsl:template match="UML:Association.connection">
	<xsl:param name="className">
		<xsl:value-of select="translate(key('classes', UML:AssociationEnd[1]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name, ' ', '_')" />
		<xsl:text>_</xsl:text>
		<xsl:value-of select="translate(key('classes', UML:AssociationEnd[2]/UML:AssociationEnd.participant/UML:Class/@xmi.idref)/@name, ' ', '_')" />
	</xsl:param>
	<xsl:if test="UML:AssociationEnd[1]//UML:MultiplicityRange/@upper = '-1' and UML:AssociationEnd[2]//UML:MultiplicityRange/@upper = '-1'">

<xsl:text>
#
class </xsl:text><xsl:value-of select="$className"/><xsl:text>Inline(admin.TabularInline):

	model = </xsl:text><xsl:value-of select="$className"/><xsl:text>
	extra = 1
</xsl:text>
	</xsl:if>
</xsl:template>

</xsl:stylesheet>