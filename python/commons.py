import dirs

tuboCode = 0            # Ordinal class code DESATUALIZADO
nadaCode = 1
confCode = 2

tuboSpCode = [1, 0, 0]  # Maximally sparse class code DESATUALIZADO
nadaSpCode = [0, 1, 0]
confSpCode = [0, 0, 1]

# String class codes used in csv files
classes = [ 'tubo', # Duto
            'nada', # Nada
            'conf', # Confuso
            'repr', # Reparo
            'dano', # Dano
            'loop', # Loop
            'corc', # Corcova
            'torc', # Torção
            'ondl', # Ondulação
            'gaio', # Gaiola de passarinho
            'corr', # Corrosão
            'ente', # Enterramento do duto
            'trin', # Trincheira
            'alte', # Alteração no duto, podendo não ser dano
            'cruz'  # Cruzamento
            ]

# Videos of the following formats are found in the data source
videoFormats = ['wmv', 'mpg', 'vob', 'avi']

# SSIM comparison threshold
ssimLim = 0.600
