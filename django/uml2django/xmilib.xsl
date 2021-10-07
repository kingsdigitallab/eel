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
<xsl:output method="text" omit-xml-declaration="yes" indent="no" />

<xsl:variable name="tag_base_classid" select="//UML:TagDefinition[@name = 'base class']/@xmi.id" />
<xsl:variable name="tag_modelid" select="//UML:TagDefinition[@name = 'model']/@xmi.id" />

<!-- ========================== -->
<!-- 		FUNCTIONS 			-->
<!-- ========================== -->

<!--  a.b.c => a.b -->
<xsl:template name="getModulePath">
	<xsl:param name="text"/>
	<xsl:param name="first-call" select="true()"/>
	<xsl:variable name="token" select="substring-before($text, '.')"/>
	<xsl:if test="string-length($token)">
		<xsl:if test="not($first-call)">.</xsl:if>
		<xsl:value-of select="$token" />
        <xsl:call-template name="getModulePath">
          <xsl:with-param name="text" select="substring-after($text, '.')"/>
          <xsl:with-param name="first-call" select="false()"/>
        </xsl:call-template>
	</xsl:if>
</xsl:template>

<!--  a.b.c => c -->
<xsl:template name="getModuleFromPath">
	<xsl:param name="text"/>
	<xsl:variable name="token" select="substring-after($text, '.')"/>
	<xsl:choose>
		<xsl:when test="string-length($token)">
	        <xsl:call-template name="getModuleFromPath">
	          <xsl:with-param name="text" select="$token"/>
	        </xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="$text" />
		</xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Here's how to do a replace() in xpath 1.0!!! -->
<xsl:template name="getQuotedText">
	<xsl:param name="text"/>
	<xsl:variable name="dquote">"</xsl:variable>
	<xsl:variable name="dquoteEscaped">\"</xsl:variable>
    <xsl:choose>
      <xsl:when test="contains($text, $dquote)">
        <xsl:variable name="bufferBefore" select="substring-before($text,$dquote)"/>
        <xsl:variable name="newBuffer" select="substring-after($text,$dquote)"/>
        <xsl:value-of select="$bufferBefore"/><xsl:value-of select="$dquoteEscaped"/>
        <xsl:call-template name="getQuotedText">
          <xsl:with-param name="text" select="$newBuffer"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="getReplacedText">
	<xsl:param name="text"/>
	<xsl:param name="source"/>
	<xsl:param name="target"/>
    <xsl:choose>
      <xsl:when test="contains($text, $source)">
        <xsl:variable name="bufferBefore" select="substring-before($text,$source)"/>
        <xsl:variable name="newBuffer" select="substring-after($text,$source)"/>
        <xsl:value-of select="$bufferBefore"/>
        <xsl:value-of select="$target"/>
        <xsl:call-template name="getReplacedText">
			<xsl:with-param name="text" select="$newBuffer"/>
			<xsl:with-param name="source" select="$source"/>
			<xsl:with-param name="target" select="$target"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="getPlural">
	<xsl:param name="class"/>
	<xsl:variable name="plural-tag-value" select="$class/UML:ModelElement.taggedValue/UML:TaggedValue[key('tags', UML:TaggedValue.type/UML:TagDefinition/@xmi.idref)/@name = 'plural']/UML:TaggedValue.dataValue/text()" />
	<xsl:choose>
		<xsl:when test="string-length($plural-tag-value) > 0"><xsl:value-of select="$plural-tag-value" /></xsl:when>
		<xsl:when test="substring($class/@name, string-length($class/@name), 1) = 'y'"><xsl:value-of select="concat(substring($class/@name, 1, string-length($class/@name) - 1), 'ies')"/></xsl:when>
		<xsl:when test="substring($class/@name, string-length($class/@name), 1) = 's'"><xsl:value-of select="concat($class/@name, 'es')"/></xsl:when>
		<xsl:otherwise><xsl:value-of select="$class/@name"/>s</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="getDjIdentifier">
	<xsl:param name="name"/>
	<xsl:value-of select="translate($name, ' ', '_')" />
</xsl:template>

<xsl:template name="getDjIdentifierL">
	<xsl:param name="name"/>
	<xsl:value-of select="translate($name, ' ABCDEFGHIJKLMNOPQRSTUVWXYZ', '_abcdefghijklmnopqrstuvwxyz')" />
</xsl:template>

<!-- use template instead of a function because we need the calling context (key and select...) -->
<xsl:template name="getParentModel">
	<xsl:param name="childid"/>
	<xsl:variable name="parentClass" select="//UML:Generalization[UML:Generalization.child/UML:Class/@xmi.idref = $childid]/UML:Generalization.parent/UML:Class" />
	<xsl:variable name="baseClassTag" select="//UML:TaggedValue[UML:TaggedValue.type/UML:TagDefinition/@xmi.idref = $tag_base_classid]/UML:TaggedValue.dataValue/text()" />
	<xsl:choose>
		<!-- xsl:when test="$parentClass"><xsl:value-of select="xmidj:getDjIdentifier(key('classes', $parentClass/@xmi.idref)/@name)" /></xsl:when -->
		<xsl:when test="$parentClass">
			<xsl:call-template name="getDjIdentifier">
				<xsl:with-param name="name"><xsl:value-of select="key('classes', $parentClass/@xmi.idref)/@name" /></xsl:with-param>
			</xsl:call-template>
		</xsl:when>
		<xsl:when test="$baseClassTag">
			<xsl:value-of select="$baseClassTag" />
		</xsl:when>
		<xsl:otherwise>models.Model</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="getShortDocQuoted">
	<xsl:param name="text"/>
	<xsl:call-template name="getQuotedText">
		<xsl:with-param name="text">
			<xsl:call-template name="getShortDoc"><xsl:with-param name="text" select="$text"/></xsl:call-template>
		</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<xsl:template name="getShortDoc">
	<!-- returns the first line of a text. If the first line starts with [, returns nothing. -->
	<xsl:param name="text"/>
	<xsl:variable name="eol"><xsl:text>&#xA;</xsl:text></xsl:variable>
	<xsl:if test="not(starts-with($text, '['))">
		<xsl:choose>
			<xsl:when test="contains($text, $eol)"><xsl:value-of select="substring-before($text, $eol)" /></xsl:when>
			<xsl:otherwise><xsl:value-of select="$text" /></xsl:otherwise>
		</xsl:choose>
	</xsl:if>
</xsl:template>

<xsl:template name="getDocField">
	<xsl:param name="text"/>
	<xsl:param name="field"/>
	<xsl:variable name="eol"><xsl:text>&#xA;</xsl:text></xsl:variable>
	<xsl:variable name="text-no-comment">
		<xsl:call-template name="getTextWithoutComments">
			<xsl:with-param name="text" select="substring-after($text, concat($eol, '#', $field, ':'))" />
		</xsl:call-template>
	</xsl:variable>
	
	<xsl:choose>
		<xsl:when test="contains($text-no-comment, concat($eol, '#'))">
			<xsl:value-of select="substring-before($text-no-comment, concat($eol, '#'))" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:value-of select="$text-no-comment" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="getLongDoc">
	<xsl:param name="text"/>

	<xsl:call-template name="getDocField">
		<xsl:with-param name="text" select="$text"/>
		<xsl:with-param name="field" select="'db-long'"/>
	</xsl:call-template>
</xsl:template>

<xsl:template name="getTextWithoutComments">
	<!-- removes all the comments from a text. Comments always starts a line with [ and ends at the next ] -->
	<xsl:param name="text"/>
	<xsl:variable name="comment"><xsl:text>&#xA;[</xsl:text></xsl:variable>
    <xsl:choose>
      <xsl:when test="contains($text, $comment)">
        <xsl:variable name="bufferBefore" select="substring-before($text,$comment)"/>
        <xsl:variable name="newBufferTemp" select="substring-after($text,$comment)"/>
        <xsl:variable name="newBuffer" select="substring-after($newBufferTemp,']')"/>
        <xsl:value-of select="$bufferBefore"/>
        <xsl:call-template name="getTextWithoutComments">
          <xsl:with-param name="text" select="$newBuffer"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="getHelpText">
	<!-- returns the help_text attribute for a field in the model. -->
	<xsl:param name="text"/>
	<xsl:param name="fieldName"/>
	<xsl:variable name="fieldNameDj"><xsl:call-template name="getDjIdentifierL"><xsl:with-param name="name" select="$fieldName"/></xsl:call-template></xsl:variable>
	<xsl:variable name="longDoc"><xsl:call-template name="getLongDoc"><xsl:with-param name="text" select="$text"/></xsl:call-template></xsl:variable>
	
	<xsl:text>help_text=ur'''</xsl:text>
	<xsl:call-template name="getShortDoc"><xsl:with-param name="text" select="$text"/></xsl:call-template>
	<xsl:if test="string-length(normalize-space($longDoc)) > 1">
		<![CDATA[<img src="/media/img/admin/icon-unknown.gif" class="long-doc-link" onclick="showLongDoc(']]><xsl:value-of select="$fieldName"/><![CDATA[', ']]><xsl:value-of select="$fieldNameDj"/><![CDATA[-doc-id');" /><span style="display:none;" id="]]><xsl:value-of select="$fieldNameDj"/><![CDATA[-doc-id">]]><xsl:value-of select="$longDoc"/><![CDATA[</span>]]>
	</xsl:if>
	<xsl:text>''', </xsl:text>

</xsl:template>

<xsl:template name="getDefaultValue">
	<xsl:param name="association" />
	<xsl:variable name="result" select="$association/UML:ModelElement.taggedValue/UML:TaggedValue[key('tags', UML:TaggedValue.type/UML:TagDefinition/@xmi.idref)/@name = 'default']/UML:TaggedValue.dataValue/text()" />
	<xsl:choose>
		<xsl:when test="string-length($result)"><xsl:value-of select="$result" /></xsl:when>
		<xsl:otherwise>1</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="getGenericForeignKey">
	<xsl:param name="fieldName" />
	<xsl:variable name="fieldNameDj"><xsl:call-template name="getDjIdentifierL"><xsl:with-param name="name" select="$fieldName"/></xsl:call-template></xsl:variable>
	<xsl:text>	</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text>_ct = models.ForeignKey(ContentType, verbose_name='</xsl:text><xsl:value-of select="$fieldName"/><xsl:text> content type', blank=True, null=True, related_name="%(class)s_</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text>_ct", </xsl:text>
	<xsl:for-each select="UML:ModelElement.taggedValue/UML:TaggedValue[(UML:TaggedValue.type/UML:TagDefinition/@xmi.idref = '-87--2--39-91--1029520:129faf30025:-8000:0000000000000EA1') or (UML:TaggedValue.type/UML:TagDefinition/@href = 'http://argouml.org/profiles/uml14/default-uml14.xmi#.:000000000000087C')]">
		<xsl:call-template name="getHelpText">
			<xsl:with-param name="text" select="UML:TaggedValue.dataValue"/>
			<xsl:with-param name="fieldName" select="$fieldName"/>
		</xsl:call-template>
	</xsl:for-each>
	<xsl:text>)
	</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text>_pk = models.PositiveIntegerField(null=True, blank=True)
	</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text> = generic.GenericForeignKey(ct_field="</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text>_ct", fk_field="</xsl:text><xsl:value-of select="$fieldNameDj"/><xsl:text>_pk")
</xsl:text>
</xsl:template>

</xsl:stylesheet>

