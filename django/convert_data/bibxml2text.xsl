<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
<xsl:output method="xml" omit-xml-declaration="no" indent="yes" />
<!-- converts the sample into the xhtml structure expected by the html templates and css -->

	<xsl:template match="/">
		<listBibl><xsl:apply-templates select="/office:document-content/office:body/office:text/text:p" /></listBibl>
		<xsl:text>&#xA;</xsl:text>
	</xsl:template>
	
	<xsl:template match="text:p">
		<bibl><xsl:apply-templates/></bibl>
	</xsl:template>
	
	<xsl:template match="text:span[@text:style-name='T5']">
		<i><xsl:apply-templates/></i>
	</xsl:template>
	
	<!-- Identity templates -->
	<xsl:template match="*">
		<xsl:apply-templates/>
	</xsl:template>
	
	<xsl:template match="text()">
		<!-- xsl:copy></xsl:copy -->
		<xsl:value-of select="normalize-space(translate(., '&#xA;&#xD;', '  '))" />
	</xsl:template>

</xsl:stylesheet>