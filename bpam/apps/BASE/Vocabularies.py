# -*- coding: UTF-8 -*-

BroadVegetationTypeVocabulary = (
    ('Marsh/bog', ''),
    ('Healthland', ''),
    ('Grassland', ''),
    ('Shrubland', ''),
    ('Woodland', ''),
    ('Forest', ''),
    ('Savannah', ''),
    ('Dune', ''),
    ('Other', ''),
)

HorizonClassificationVocabulary = (
    ('O horizon',
     'The organic or litter layer mainly over the soil surface composed of fresh and decaying plant residue. Typically composed of >25% organic soil materials.  This layer can usually be easily brushed away by hand.'),
    ('A horizon',
     'This is the top layer of soil (often called top soil) that typically has the highest microbial activity.  It is composed of a mixture of mineral material and accumulated humified organic matter. Also, any plowed or disturbed surface layer.'),
    ('E horizon',
     'This is the eluviated layer that is only seen in older soils and is not a universally used horizon designation.  If present it is below the A horizon and commonly is recognized by its lighter colored due to loss of clay, iron, aluminum, organic matter or some combination of these components.'),
    ('B horizon',
     'In lay terms this is often called sub-soil.  It is the layer where most of the mineral materials that leach from the upper horizons accumulate.  Accumulation of clay, iron, silica, calcium carbonate, calcium sulphate, sesquioxides, and/or humus can occur.  Soil structure and color often differs from the A horizon. Color may be redder or browner due to iron accumulation.  Structure may be more granular, prismatic, or blocky.'),
    ('C horizon',
     'This is basically the weathered parent rock (excluding hard bedrock) that has not been affected by soil formation.  Composed mainly of large rocks.'),
    ('R layer',
     'This is the consolidated unweathered hard bedrock beneath the soil.  Usually is one large continuous rock mass.  The bedrock commonly found below the C horizon but under certain circumstances can be found directly below the A or B horizon.'),
    ('Permafrost',
     'Soils that are permanently frozen due to sustained temperature of less than 0ºC for two or more years.  Typically found in Polar regions.'),
)

ProfilePositionVocabulary = (
    ('Summit/ridge', ''),
    ('Upper slope', ''),
    ('Mid slope', ''),
    ('Lower slope', ''),
    ('Valley floor', ''),
    ('Depression', ''),
)

DrainageClassificationVocabulary = (
    ('Excessively drained',
     'Water is removed from the soil very rapidly and available water holding capacity is very low.  Soils are commonly very sandy, gravelly or shallow on steep slopes All are uniform color and free of the mottling (mixture of colors in the same layer, often yellow, brown and sometimes grey) related to wetness. Irrigation would be needed for crop production.'),
    ('Somewhat excessively drained',
     'Water is removed from the soil rapidly. Internal free water occurrence commonly is very rare or very deep. The soils are commonly coarse-textured and have high saturated hydraulic conductivity or are very shallow.'),
    ('Well drained',
     'Water is removed from the soil readily, but not rapidly making it available to plants throughout most of the growing season.  Seasonal high water table is not within the rooting zone long enough during the growing season to adversely affect agricultural crops. Soils are commonly medium textured and mainly free of mottling.'),
    ('Moderately well drained',
     'Water is removed from the soil somewhat slowly during some periods. Soils are wet for only a short time during the growing season, but periodically they are wet long enough that most mesophytic crops are affected. They commonly have a slowly pervious layer within or directly below the solum, or periodically receive high rainfall, or both.'),
    ('Somewhat poorly drained',
     'Water is removed slowly enough that the soil is wet for significant periods during the growing season. Wetness markedly restricts the growth of mesophytic crops unless artificial drainage is provided. Soils commonly have a slowly pervious layer, a high water table, additional water from seepage, nearly continuous rainfall, or a combination of these factors.'),
    ('Poorly drained',
     'Water is removed so slowly that the soil is saturated periodically during the growing season or remains wet for long periods. Free water is commonly at or near the surface for long enough during the growing season that most mesophytic crops cannot be grown unless the soil is artificially drained. The soil is not continuously saturated in layers directly below plow depth. Poor drainage results from a high water table, a slowly pervious layer within the profile, seepage, nearly continuous rainfall, or a combination of these.'),
    ('Very poorly drained',
     'Water is removed from the soil so slowly that free water remains at or on the surface during most of the growing season. Unless the soil is artificially drained, most mesophytic crops cannot be grown. Very poorly drained soils are commonly level or depressed and are frequently ponded. Yet in rare cases, where rainfall is high and nearly continuous, they can have moderate or high slope gradients.'),
)

SoilClassificationVocabulary = (
    ('AUS', 'Anthroposols'),
    ('AUS', 'Organosols'),
    ('AUS', 'Podosols'),
    ('AUS', 'Vertosols'),
    ('AUS', 'Hydrosols'),
    ('AUS', 'Kurosols'),
    ('AUS', 'Sodosols'),
    ('AUS', 'Chromosols'),
    ('AUS', 'Calcarosols'),
    ('AUS', 'Ferrosols'),
    ('AUS', 'Dermosols'),
    ('AUS', 'Kandosols'),
    ('AUS', 'Rudosols'),
    ('AUS', 'Tenosols'),
    ('FAO', 'HISTOSOLS'),
    ('FAO', 'CRYOSOLS'),
    ('FAO', 'NTHROSOLS'),
    ('FAO', 'LEPTOSOLS'),
    ('FAO', 'VERTISOLS'),
    ('FAO', 'FLUVISOLS'),
    ('FAO', 'SOLONCHAKS'),
    ('FAO', 'GLEYSOLS'),
    ('FAO', 'ANDOSOLS'),
    ('FAO', 'PODZOLS'),
    ('FAO', 'PLINTHOSOLS'),
    ('FAO', 'FERRALSOLS'),
    ('FAO', 'SOLONETZ'),
    ('FAO', 'PLANOSOLS'),
    ('FAO', 'CHERNOZEMS'),
    ('FAO', 'KASTANOZEMS'),
    ('FAO', 'PHAEOZEMS'),
    ('FAO', 'GYPSISOLS'),
    ('FAO', 'DURISOLS'),
    ('FAO', 'CALCISOLS'),
    ('FAO', 'ALBELUVISOLS'),
    ('FAO', 'ALISOLS'),
    ('FAO', 'NITISOLS'),
    ('FAO', 'ACRISOLS'),
    ('FAO', 'LUVISOLS'),
    ('FAO', 'LIXISOLS'),
    ('FAO', 'UMBRISOLS'),
    ('FAO', 'CAMBISOLS'),
    ('FAO', 'ARENOSOLS'),
    ('FAO', 'REGOSOLS'),
)

SoilColourVocabulary = (
    ('Brown', 'BR'),
    ('Gray', 'GR'),
    ('Black', 'BK'),
    ('Brown Gray', 'BRGR'),
    ('Gray Brown', 'GRBR'),
    ('Light Brown', 'LTBR'),
    ('Dark Brown', 'DKBR'),
    ('Light Gray', 'LTGR'),
    ('Dark Gray', 'DKGR'),
    ('Brown Yellow', 'BRYW'),
    ('Brown Red', 'BRRD'),
    ('Brown Orange', 'BROR'),
    ('Brown Black', 'BRBK'),
    ('Brown White', 'BRWH'),
    ('Gray Black', 'GRBK'),
    ('Gray White', 'GRWH'),
    ('Gray Yellow', 'GRYW'),
    ('White', 'WH'),
    ('Yellow', 'YW'),
    ('Yellow Brown', 'YWBR'),
    ('Yellow Gray', 'YWGR'),
    ('Orange', 'OR'),
)

SoilTextureVocabulary = (
    ('Clay', '<2 µm'),
    ('Silt', '2-20 µm'),
    ('Fine sand', '20-200 µm'),
    ('Course sand', '200-2000 µm'),
    ('Sand', 'Total of fine and coarse sand'),
    ('Gravel', '>2.0 mm'),
)


def load(orm):
    for vegetation, note in BroadVegetationTypeVocabulary:
        t = orm.BroadVegetationType.objects.create()
        t.vegetation = vegetation
        t.note = note
        t.save()

    for horizon, description in HorizonClassificationVocabulary:
        t = orm.HorizonClassification.objects.create()
        t.horizon = horizon
        t.description = description
        t.save()

    for position, _ in ProfilePositionVocabulary:
        t = orm.ProfilePosition.objects.create(position=position)
        t.save()

    for drainage, description in DrainageClassificationVocabulary:
        t = orm.DrainageClassification.objects.create()
        t.drainage = drainage
        t.description = description
        t.save()

    for authority, classification in SoilClassificationVocabulary:
        t = orm.SoilClassification.objects.create()
        t.authority = authority
        t.classification = classification
        t.save()

    for colour, code in SoilColourVocabulary:
        t = orm.SoilColour.objects.create()
        t.colour = colour
        t.code = code
        t.save()

    for texture, description in SoilTextureVocabulary:
        t = orm.SoilTexture.objects.create()
        t.texture = texture
        t.description = description
        t.save()