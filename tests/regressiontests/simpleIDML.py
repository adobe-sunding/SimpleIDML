# -*- coding: utf-8 -*-

import os, sys, shutil
import glob
import unittest
import codecs
import StringIO
from decimal import Decimal
from tempfile import mkdtemp 
from lxml import etree

from simple_idml.idml import IDMLPackage
from simple_idml.idml import XMLDocument
from simple_idml.idml import Spread, Story
from simple_idml.idml import RECTO, VERSO

CURRENT_DIR = os.path.dirname(__file__)
IDMLFILES_DIR = os.path.join(CURRENT_DIR, "simpleIDML_files")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "outputs", "simpleIDML")


class SimpleIDMLTestCase(unittest.TestCase):
    def setUp(self):
        super(SimpleIDMLTestCase, self).setUp()
        for f in glob.glob(os.path.join(OUTPUT_DIR, "*")):
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.unlink(f)

    def test_idml_package(self):
        idml_file = os.path.join(IDMLFILES_DIR, "4-pages.idml")
        idml_file = IDMLPackage(idml_file)
        
        # Spreads.
        self.assertEqual(idml_file.spreads, [u'Spreads/Spread_ub6.xml',
                                             u'Spreads/Spread_ubc.xml',
                                             u'Spreads/Spread_uc3.xml'])

        # Stories.
        self.assertEqual(idml_file.stories, [u'Stories/Story_u139.xml',
                                             u'Stories/Story_u11b.xml',
                                             u'Stories/Story_u102.xml',
                                             u'Stories/Story_ue4.xml'])
        story = idml_file.get_story_object_by_id("u139")
        self.assertEqual(story.node.tag, "Story")

        # Tags.
        self.assertEqual([etree.tostring(tag) for tag in idml_file.tags], 
                        ['<XMLTag Self="XMLTag/advertise" Name="advertise">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Green</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/article" Name="article">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Red</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/content" Name="content">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Magenta</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/description" Name="description">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Gray</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/illustration" Name="illustration">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Cyan</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t', 
                         '<XMLTag Self="XMLTag/Root" Name="Root">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">LightBlue</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/Story" Name="Story">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">BrickRed</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/subtitle" Name="subtitle">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Yellow</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n\t',
                         '<XMLTag Self="XMLTag/title" Name="title">\n\t\t<Properties>\n\t\t\t<TagColor type="enumeration">Blue</TagColor>\n\t\t</Properties>\n\t</XMLTag>\n'])

        # Styles.
        self.assertEqual([style.tag for style in idml_file.style_groups], ['RootCharacterStyleGroup',
                                                                           'RootParagraphStyleGroup',
                                                                           'RootCellStyleGroup',
                                                                           'RootTableStyleGroup',
                                                                           'RootObjectStyleGroup'])

        # Fonts.
        self.assertEqual([font.get("Name") for font in idml_file.font_families], ['Minion Pro', 'Myriad Pro', 'Kozuka Mincho Pro', 'Vollkorn'])

        # XML Structure.
       # print"\n", (etree.tostring(idml_file.XMLStructure.dom, pretty_print=True))
        self.assertEqual(etree.tostring(idml_file.XMLStructure.dom, pretty_print=True),
"""<Root Self="di2">
  <article XMLContent="u102" Self="di2i3">
    <Story XMLContent="ue4" Self="di2i3i1">
      <title Self="di2i3i1i1"/>
      <subtitle Self="di2i3i1i2"/>
    </Story>
    <content XMLContent="u11b" Self="di2i3i2"/>
    <illustration XMLContent="u135" Self="di2i3i3"/>
    <description XMLContent="u139" Self="di2i3i4"/>
  </article>
  <article XMLContent="udb" Self="di2i4"/>
  <article XMLContent="udd" Self="di2i5"/>
  <advertise XMLContent="udf" Self="di2i6"/>
</Root>
""")

        # Test a file with a slighly different structure
        idml_file = os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs.idml")
        idml_file = IDMLPackage(idml_file)
        #print"\n", (etree.tostring(idml_file.XMLStructure.dom, pretty_print=True))
        self.assertEqual(etree.tostring(idml_file.XMLStructure.dom, pretty_print=True), 
"""<Root Self="di2">
  <page Self="di2ib">
    <title XMLContent="u1b2" Self="di2ibi34"/>
    <article XMLContent="u1c9" Self="di2ibi33"/>
    <article XMLContent="u1e0" Self="di2ibi32"/>
    <article XMLContent="u1fb" Self="di2ibi31"/>
    <article XMLContent="u212" Self="di2ibi30"/>
  </page>
  <page Self="di2i10">
    <advertise XMLContent="u278" Self="di2i10i36"/>
  </page>
</Root>
""")

    def test_get_story_by_xpath(self):
        idml_file = os.path.join(IDMLFILES_DIR, "4-pages.idml")
        idml_file = IDMLPackage(idml_file)
        self.assertEqual(idml_file.get_story_by_xpath("/Root/article[1]"), "XML/BackingStory.xml")
        self.assertEqual(idml_file.get_story_by_xpath("/Root/article[1]/Story"), "Stories/Story_u102.xml")
        self.assertEqual(idml_file.get_story_by_xpath("/Root/article[1]/Story/title"), "Stories/Story_ue4.xml")
        self.assertEqual(idml_file.get_story_by_xpath("/Root/article[1]/illustration"), "Stories/Story_u102.xml")
            
    def test_namelist(self):
        # The namelist can be inherited from ZipFile or computed from the working copy.
        idml_file = os.path.join(IDMLFILES_DIR, "4-pages.idml")
        idml_file = IDMLPackage(idml_file)
        zipfile_namelist = idml_file.namelist()

        idml_working_copy = mkdtemp()
        idml_file.extractall(idml_working_copy)
        idml_file.working_copy_path = idml_working_copy
        idml_file.init_lazy_references()

        working_copy_namelist = idml_file.namelist()
        self.assertEqual(set(zipfile_namelist), set(working_copy_namelist))

        shutil.rmtree(idml_working_copy)

    def test_export_xml(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "article-1photo_import-xml.idml"))
        xml = idml_file.export_xml()
        self.assertEqual(xml, 
"""<Root>
  <module>
    <main_picture/>
    <headline>THE HEADLINE HERE</headline>
    <Story>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt.Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt.<article/><informations/></Story>
  </module>
</Root>
""")

    def test_prefix(self):
        shutil.copy2(os.path.join(IDMLFILES_DIR, "4-pages.idml"), 
                     os.path.join(OUTPUT_DIR, "4-pages.idml"))

        idml_file = IDMLPackage(os.path.join(OUTPUT_DIR, "4-pages.idml"))
        idml_file = idml_file.prefix("FOO")

        # Spreads.
        self.assertEqual(idml_file.spreads, ['Spreads/Spread_FOOub6.xml',
                                             'Spreads/Spread_FOOubc.xml',
                                             'Spreads/Spread_FOOuc3.xml'])
        spread = etree.fromstring(idml_file.open("Spreads/Spread_FOOub6.xml").read())
        self.assertEqual(spread.xpath(".//Spread[1]")[0].get("Self"), "FOOub6")
        self.assertEqual(spread.xpath(".//Spread[1]/Page[1]")[0].get("Self"), "FOOubb")
        self.assertEqual(spread.xpath(".//Spread[1]/TextFrame[1]")[0].get("Self"), "FOOud8")
        self.assertEqual(spread.xpath(".//Spread[1]/TextFrame[1]")[0].get("ParentStory"), "FOOu102")

        # Stories.
        self.assertEqual(idml_file.stories, ['Stories/Story_FOOu102.xml',
                                             'Stories/Story_FOOu11b.xml',
                                             'Stories/Story_FOOu139.xml',
                                             'Stories/Story_FOOue4.xml'])
        story = etree.fromstring(idml_file.open("Stories/Story_FOOu102.xml").read())
        self.assertEqual(story.xpath("//CharacterStyleRange")[0].get("AppliedCharacterStyle"),
                         "FOOCharacterStyle/$ID/[No character style]")

        # XML Structure.
        self.assertEqual(etree.tostring(idml_file.XMLStructure.dom, pretty_print=True),
"""<Root Self="FOOdi2">
  <article XMLContent="FOOu102" Self="FOOdi2i3">
    <Story XMLContent="FOOue4" Self="FOOdi2i3i1">
      <title Self="FOOdi2i3i1i1"/>
      <subtitle Self="FOOdi2i3i1i2"/>
    </Story>
    <content XMLContent="FOOu11b" Self="FOOdi2i3i2"/>
    <illustration XMLContent="FOOu135" Self="FOOdi2i3i3"/>
    <description XMLContent="FOOu139" Self="FOOdi2i3i4"/>
  </article>
  <article XMLContent="FOOudb" Self="FOOdi2i4"/>
  <article XMLContent="FOOudd" Self="FOOdi2i5"/>
  <advertise XMLContent="FOOudf" Self="FOOdi2i6"/>
</Root>
""")
        # designmap.xml
        designmap = etree.fromstring(idml_file.open("designmap.xml").read())
        self.assertEqual(designmap.xpath("/Document")[0].get("StoryList"),
                         "FOOue4 FOOu102 FOOu11b FOOu139 FOOu9c")
        self.assertEqual(designmap.xpath(".//idPkg:Story", 
                                  namespaces={'idPkg': "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"})[0].get("src"),
                        "Stories/Story_FOOu139.xml")
        self.assertEqual(designmap.xpath(".//idPkg:Spread", 
                                  namespaces={'idPkg': "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"})[0].get("src"),
                        "Spreads/Spread_FOOub6.xml")
                                   
    def test_insert_idml(self):
        shutil.copy2(os.path.join(IDMLFILES_DIR, "4-pages.idml"), 
                     os.path.join(OUTPUT_DIR, "4-pages.idml"))
        shutil.copy2(os.path.join(IDMLFILES_DIR, "article-1photo.idml"), 
                     os.path.join(OUTPUT_DIR, "article-1photo.idml"))

        main_idml_file = IDMLPackage(os.path.join(OUTPUT_DIR, "4-pages.idml"))
        article_idml_file = IDMLPackage(os.path.join(OUTPUT_DIR, "article-1photo.idml"))

        # Always start by prefixing packages to avoid collision.
        main_idml_file = main_idml_file.prefix("main")
        article_idml_file = article_idml_file.prefix("article1")

        main_idml_file = main_idml_file.insert_idml(article_idml_file, 
                                                    at="/Root/article[3]",
                                                    only="/Root/module[1]")

        # Stories.
        self.assertEqual(main_idml_file.stories, ['Stories/Story_article1u188.xml',
                                                  'Stories/Story_article1u19f.xml',
                                                  'Stories/Story_article1u1db.xml', 
                                                  'Stories/Story_mainu102.xml',
                                                  'Stories/Story_mainu11b.xml', 
                                                  'Stories/Story_mainu139.xml',
                                                  'Stories/Story_mainue4.xml'])

        # The XML Structure has integrated the new file.
        #print"\n", (etree.tostring(main_idml_file.XMLStructure.dom, pretty_print=True))
        self.assertEqual(etree.tostring(main_idml_file.XMLStructure.dom, pretty_print=True),
"""<Root Self="maindi2">
  <article XMLContent="mainu102" Self="maindi2i3">
    <Story XMLContent="mainue4" Self="maindi2i3i1">
      <title Self="maindi2i3i1i1"/>
      <subtitle Self="maindi2i3i1i2"/>
    </Story>
    <content XMLContent="mainu11b" Self="maindi2i3i2"/>
    <illustration XMLContent="mainu135" Self="maindi2i3i3"/>
    <description XMLContent="mainu139" Self="maindi2i3i4"/>
  </article>
  <article XMLContent="mainudb" Self="maindi2i4"/>
  <article Self="maindi2i5">
    <module XMLContent="article1u1db" Self="article1di3i12">
      <main_picture XMLContent="article1u182" Self="article1di3i12i1"/>
      <headline XMLContent="article1u188" Self="article1di3i12i2"/>
      <Story XMLContent="article1u19f" Self="article1di3i12i3">
        <article Self="article1di3i12i3i2"/>
        <informations Self="article1di3i12i3i1"/>
      </Story>
    </module>
  </article>
  <advertise XMLContent="mainudf" Self="maindi2i6"/>
</Root>
""")

        # Designmap.xml.
        designmap = etree.fromstring(main_idml_file.open("designmap.xml", mode="r").read())
        self.assertEqual(designmap.xpath("/Document")[0].get("StoryList"),
                         "mainue4 mainu102 mainu11b mainu139 mainu9c article1u188 article1u19f article1u1db")
        self.assertEqual(len(designmap.xpath("/Document/idPkg:Story",
                             namespaces={'idPkg': "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"})), 7)

        # TODO Test Spread_mainub6.xml content.

        # Styles.
        self.assertEqual([[style.get("Self") for style in style_group.iterchildren()] for style_group in main_idml_file.style_groups], 
                         [['mainCharacterStyle/$ID/[No character style]',
                           'article1CharacterStyle/$ID/[No character style]'],
                          ['mainParagraphStyle/$ID/[No paragraph style]',
                           'mainParagraphStyle/$ID/NormalParagraphStyle', 
                           'article1ParagraphStyle/$ID/[No paragraph style]',
                           'article1ParagraphStyle/$ID/NormalParagraphStyle'],
                          ['mainCellStyle/$ID/[None]', 'article1CellStyle/$ID/[None]'],
                          ['mainTableStyle/$ID/[No table style]',
                           'mainTableStyle/$ID/[Basic Table]', 
                           'article1TableStyle/$ID/[No table style]',
                           'article1TableStyle/$ID/[Basic Table]'],
                          ['mainObjectStyle/$ID/[None]',
                           'mainObjectStyle/$ID/[Normal Graphics Frame]',
                           'mainObjectStyle/$ID/[Normal Text Frame]',
                           'mainObjectStyle/$ID/[Normal Grid]', 
                           'article1ObjectStyle/$ID/[None]', 
                           'article1ObjectStyle/$ID/[Normal Graphics Frame]',
                           'article1ObjectStyle/$ID/[Normal Text Frame]', 
                           'article1ObjectStyle/$ID/[Normal Grid]']
                         ])

    def test_add_page_from_idml(self):
        edito_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-edito.idml")
        courrier_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-courrier-des-lecteurs.idml")
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-edito.idml"), edito_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs.idml"), courrier_idml_filename)

        edito_idml_file = IDMLPackage(edito_idml_filename)
        courrier_idml_file = IDMLPackage(courrier_idml_filename)

        # Always start by prefixing packages to avoid collision.
        edito_idml_file = edito_idml_file.prefix("edito")
        courrier_idml_file = courrier_idml_file.prefix("courrier")
        self.assertEqual(len(edito_idml_file.pages), 2)

        new_idml = edito_idml_file.add_page_from_idml(courrier_idml_file,
                                                      page_number=1,
                                                      at="/Root",
                                                      only="/Root/page[1]")
        self.assertEqual(len(new_idml.pages), 3)

        # The XML Structure has integrated the new file.
        #print"\n", (etree.tostring(new_idml.XMLStructure.dom, pretty_print=True))
        self.assertEqual(etree.tostring(new_idml.XMLStructure.dom, pretty_print=True),
"""<Root Self="editodi2">
  <page Self="editodi2ib">
    <article Self="editodi2ibif">
      <Story XMLContent="editoue4" Self="editodi2ibifi1f">
        <title Self="editodi2ibifi1fi1"/>
        <subtitle Self="editodi2ibifi1fi2"/>
      </Story>
      <content XMLContent="editou11b" Self="editodi2ibifi1e"/>
    </article>
  </page>
  <page Self="editodi2i10">
    <advertise XMLContent="editou1de" Self="editodi2i10i23"/>
  </page>
  <page Self="courrierdi2ib">
    <title XMLContent="courrieru1b2" Self="courrierdi2ibi34"/>
    <article XMLContent="courrieru1c9" Self="courrierdi2ibi33"/>
    <article XMLContent="courrieru1e0" Self="courrierdi2ibi32"/>
    <article XMLContent="courrieru1fb" Self="courrierdi2ibi31"/>
    <article XMLContent="courrieru212" Self="courrierdi2ibi30"/>
  </page>
</Root>
""")

    def test_add_pages_from_idml(self):
        edito_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-edito.idml")
        courrier_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-courrier-des-lecteurs.idml")
        bloc_notes_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-bloc-notes.idml")
        bloc_notes2_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-bloc-notes2.idml")
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-edito.idml"), edito_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs.idml"), courrier_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-bloc-notes.idml"), bloc_notes_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-bloc-notes.idml"), bloc_notes2_idml_filename)

        edito_idml_file = IDMLPackage(edito_idml_filename)
        courrier_idml_file = IDMLPackage(courrier_idml_filename)
        bloc_notes_idml_file = IDMLPackage(bloc_notes_idml_filename)
        bloc_notes2_idml_file = IDMLPackage(bloc_notes2_idml_filename)

        # Always start by prefixing packages to avoid collision.
        edito_idml_file = edito_idml_file.prefix("edito")
        courrier_idml_file = courrier_idml_file.prefix("courrier")
        bloc_notes_idml_file = bloc_notes_idml_file.prefix("blocnotes")
        bloc_notes2_idml_file = bloc_notes2_idml_file.prefix("blocnotes2")

        packages_to_add = [
            (courrier_idml_file, 1, "/Root", "/Root/page[1]"),
            (bloc_notes_idml_file, 1, "/Root", "/Root/page[1]"),
            (bloc_notes2_idml_file, 2, "/Root", "/Root/page[2]"),
        ]

        new_idml = edito_idml_file.add_pages_from_idml(packages_to_add)
        os.unlink(courrier_idml_filename)
        os.unlink(bloc_notes_idml_filename)
        os.unlink(bloc_notes2_idml_filename)

        self.assertEqual(len(new_idml.pages), 5)
        self.assertEqual(new_idml.spreads, ['Spreads/Spread_editoub6.xml',
                                            'Spreads/Spread_editoubc.xml', 
                                            'Spreads/Spread_editoubd.xml'])

    def test_add_pages_from_idml_to_template(self):
        # Now we use an empty document to hold the pages.
        magazineA_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-template.idml")
        edito_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-edito.idml")
        courrier_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-courrier-des-lecteurs.idml")
        bloc_notes_idml_filename = os.path.join(OUTPUT_DIR, "magazineA-bloc-notes.idml")
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-template.idml"), magazineA_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-edito.idml"), edito_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs.idml"), courrier_idml_filename)
        shutil.copy2(os.path.join(IDMLFILES_DIR, "magazineA-bloc-notes.idml"), bloc_notes_idml_filename)

        magazineA_idml_file = IDMLPackage(magazineA_idml_filename)
        edito_idml_file = IDMLPackage(edito_idml_filename)
        courrier_idml_file = IDMLPackage(courrier_idml_filename)
        bloc_notes_idml_file = IDMLPackage(bloc_notes_idml_filename)

        # Always start by prefixing packages to avoid collision.
        magazineA_idml_file = magazineA_idml_file.prefix("mag")
        edito_idml_file = edito_idml_file.prefix("edito")
        courrier_idml_file = courrier_idml_file.prefix("courrier")
        bloc_notes_idml_file = bloc_notes_idml_file.prefix("blocnotes")

        packages_to_add = [
            (edito_idml_file, 1, "/Root", "/Root/page[1]"),
            (courrier_idml_file, 1, "/Root", "/Root/page[1]"),
            (bloc_notes_idml_file, 1, "/Root", "/Root/page[1]"),
        ]

        magazineA_idml_file = magazineA_idml_file.add_pages_from_idml(packages_to_add)
        os.unlink(edito_idml_filename)
        os.unlink(courrier_idml_filename)
        os.unlink(bloc_notes_idml_filename)

        self.assertEqual(len(magazineA_idml_file.pages), 4)
        self.assertEqual(magazineA_idml_file.spreads, ['Spreads/Spread_magub6.xml', 'Spreads/Spread_magub7.xml'])

class XMLDocumentTestCase(unittest.TestCase):
    def test_get_element_by_id(self):
        xml_file = open(os.path.join(IDMLFILES_DIR, "4-pages.idml Folder", "Stories", "Story_ue4.xml"), mode="r")
        doc = XMLDocument(xml_file)
        elt = doc.getElementById("di2i3i1")
        self.assertTrue(elt is not None)

    # TODO: move this test to the subclasses of IDMLXMLFile.
    def test_to_string(self):
        xml_file = StringIO.StringIO()
        xml_file.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                          <document>This is a XML document with unicode : ₣.</document>""")
        xml_file.seek(0)
        doc = XMLDocument(xml_file)
        self.assertEqual(doc.tostring(), """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<document>This is a XML document with unicode : ₣.</document>
""")
        self.assertEqual(doc.tostring(ref_doctype="designmap.xml"), """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="7.5(142)" ?>
<document>This is a XML document with unicode : ₣.</document>
""")

class SpreadTestCase(unittest.TestCase):
    def test_pages(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "4-pages.idml"), mode="r")
        spreads = idml_file.spreads

        spread1 = Spread(idml_file, spreads[0])
        spread1_pages = spread1.pages
        self.assertEqual(len(spread1_pages), 1)
        self.assertEqual(spread1_pages[0].node.tag, "Page")

        spread2 = Spread(idml_file, spreads[1])
        spread2_pages = spread2.pages
        self.assertEqual(len(spread2_pages), 2)
        self.assertEqual(spread2_pages[0].node.tag, "Page")
        self.assertEqual(spread2_pages[1].node.tag, "Page")

class StoryTestCase(unittest.TestCase):
    def test_pages(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "4-pages.idml"), mode="r")
        stories = idml_file.stories

        story = Story(idml_file, stories[0])
        self.assertEqual(story.node.tag, "Story")

    def test_get_element_by_id(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "4-pages.idml"), mode="r")
        story = idml_file.get_story_object_by_id("u11b")
        elem = story.get_element_by_id("di2i3i2")
        self.assertEqual(elem.get("MarkupTag"), "XMLTag/content")

    def test_get_element_content_by_id(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "4-pages.idml"), mode="r")
        story = idml_file.get_story_object_by_id("u11b")
        content = story.get_element_content_by_id("di2i3i2")
        self.assertEqual(content, u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\u2029Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?')

class PageTestCase(unittest.TestCase):
    def test_page_items(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs-3pages.idml"), mode="r")
        spread = Spread(idml_file, idml_file.spreads[1])

        page1 = spread.pages[0]
        self.assertEqual([i.tag for i in page1.page_items], ["Rectangle"])

        page2 = spread.pages[1]
        self.assertEqual([i.tag for i in page2.page_items], [
            'Rectangle',
            'TextFrame',
            'Polygon',
            'Polygon',
            'Polygon',
            'GraphicLine',
            'Polygon',
            'Polygon',
            'Oval',
            'Rectangle',
        ])
        
        # test the setter
        page2.page_items = ["foo", "bar"]
        self.assertEqual(page2.page_items, ["foo", "bar"])

    def test_coordinates(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs-3pages.idml"), mode="r")
        spread = Spread(idml_file, idml_file.spreads[1])

        page2 = spread.pages[0]
        self.assertEqual(page2.coordinates, {
            'x1': Decimal('-566.9291338582677'),
            'y1': Decimal('-379.8425196850394'),
            'x2': Decimal('0E-13'),
            'y2': Decimal('379.8425196850394')
        })

        page3 = spread.pages[1]
        self.assertEqual(page3.coordinates, {
            'x1': Decimal('0'),
            'y1': Decimal('-379.8425196850394'),
            'x2': Decimal('566.9291338582677'),
            'y2': Decimal('379.8425196850394'),
        })

    def test_is_recto(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs-3pages.idml"), mode="r")
        spread1 = Spread(idml_file, idml_file.spreads[0])
        page1 = spread1.pages[0]
        self.assertTrue(page1.is_recto)

        spread2 = Spread(idml_file, idml_file.spreads[1])
        page2 = spread2.pages[0]
        page3 = spread2.pages[1]
        self.assertFalse(page2.is_recto)
        self.assertTrue(page3.is_recto)

    def test_set_face(self):
        idml_file = IDMLPackage(os.path.join(IDMLFILES_DIR, "magazineA-courrier-des-lecteurs.idml"), mode="r")
        spread2 = Spread(idml_file, idml_file.spreads[1])
        page2 = spread2.pages[0]
        self.assertEqual(page2.face, VERSO)
        
        page2.set_face(RECTO)
        self.assertEqual(page2.face, RECTO)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleIDMLTestCase)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(XMLDocumentTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SpreadTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(StoryTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PageTestCase))
    return suite
