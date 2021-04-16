#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import seaborn as sns
import pylab as pl
import glob, os

pl.rc('text', usetex=True)
pl.rc('font', family='serif',  serif='Times')

    
fd = 'Relatório de Consolidação de Programa'
fn = glob.glob(fd+'/*.xls')

A = pd.DataFrame()
for io in fn:
    df = pd.read_csv(io, sep='\t', encoding = "ISO-8859-1",)
    
    A=pd.concat([A,df])
    

c = [
       'Instituição de Ensino', 'Programa', 'Ano Referência',
       'Discente - Doutorado - MATRICULADO', 'Discente - Doutorado - TITULADO',
       'Discente - Doutorado - DESLIGADO', 'Discente - Doutorado - ABANDONOU',
       'Discente - Doutorado - Total Ativos',
       'Discente - Doutorado - Total Inativos', 'Discente - Doutorado - Total',
       'Discente - Doutorado - Tempo médio de titulação(Meses)',
       'Discente - Mestrado - MATRICULADO', 'Discente - Mestrado - TITULADO',
       'Discente - Mestrado - DESLIGADO', 'Discente - Mestrado - ABANDONOU',
       'Discente - Mestrado - MUDANCA DE NÍVEL SEM DEFESA',
       'Discente - Mestrado - MUDANCA DE NÍVEL COM DEFESA',
       'Discente - Mestrado - Total Ativos',
       'Discente - Mestrado - Total Inativos', 'Discente - Mestrado - Total',
       'Discente - Mestrado - Tempo médio de titulação(Meses)',
       'Docente - Permanente', 'Docente - Colaborador', 'Docente - Visitante',
       'Docente - Total', 'Participante Externo', 'Pós-Doc',
       'Egresso - Mestrado Acadêmico', 'Egresso - Total', 'Disciplinas',
       'Financiadores', 'Turmas',
       'Turmas Associadas a Projetos de Cooperação entre Instituições',
       'Áreas de Concentração', 'Linhas de Pesquisa',
       'Projetos de Pesquisa Em Andamento', 'Projetos de Pesquisa Concluídos',
       'Produção - ARTÍSTICO-CULTURAL Com participação de discentes',
       'Produção - ARTÍSTICO-CULTURAL Sem participação de discentes',
       'Total de Produções ARTÍSTICO-CULTURAL(S)',
       'Produção - BIBLIOGRÁFICA Com participação de discentes',
       'Produção - BIBLIOGRÁFICA Sem participação de discentes',
       'Total de Produções BIBLIOGRÁFICA(S)',
       'Produção - TÉCNICA Com participação de discentes',
       'Produção - TÉCNICA Sem participação de discentes',
       'Total de Produções TÉCNICA(S)',
       'Trabalhos de Conclusão de Nível Doutorado',
       'Trabalhos de Conclusão de Nível Mestrado',
       'Total de Trabalhos de Conclusão', 'Egresso - Doutorado',
       ]

A = A.fillna(np.nan).replace([np.nan], [None],)
A.columns = [x.replace('Discente - ','') for x in A.columns]
c = list(A.columns)
    
for (a,b), df in A.groupby([c[0],c[1]]):
    dir_name = './figuras/'+a+' - '+b
    dir_name = dir_name.replace(' ','_')
    os.system('mkdir -p '+dir_name)
    
    keys=[
        ('Corpo Discente - Doutorado'           , c[2:3]+c[3:10]  ),
        ('Corpo Discente - Mestrado'            , c[2:3]+c[11:20] ),        
        ('Tempo médio de titulação(Meses)'      , c[2:3]+c[10:11] +c[20:21] ),        
        ('Docentes'                             , c[2:3]+c[21:25] ),        
        ('Participantes Externos'               , c[2:3]+c[25:26] ),        
        ('Egressos'                             , c[2:3]+c[27:29]+c[49:50]),        
        ('Egressos Doutorado'                   , c[2:3]+c[27:28] ),        
        ('Egressos Mestado  '                   , c[2:3]+c[28:29] ),        
        ('Disciplinas e Turmas'                 , c[2:3]+c[30:31] ),
        ('Produção Artística-Cultural'          , c[2:3]+c[38:41] ),
        ('Produção Bibliográfica'               , c[2:3]+c[41:44] ),
        ('Produção Técnica'                     , c[2:3]+c[44:47] ),
        ('Trabalhos de Conclusão'               , c[2:3]+c[47:49] ),
        ]   
    
    
    for key, key_col in keys:
        aux = df[key_col]
        aux.dropna(inplace=True)
        aux=aux.astype(int)
        n_colors = aux.shape[1]-1
        palette=sns.color_palette("tab10")[:n_colors]
        aux=aux.melt(id_vars=c[2])
        #%%
        pl.figure()
        a4_dims = (4, 6)
        fig, ax = pl.subplots()#figsize=a4_dims)
        for (label, item), color in zip(aux.groupby('variable'),palette):
            g = sns.lineplot(x=c[2], y='value', hue='variable', style='variable', 
                          markers=True, dashes=False, 
                          data=item, 
                          palette=(color,),
                          )
            s=item[c[2]].unique(); s.sort(); g.set_xticks(s);
            for x,y,m in item[[c[2],'value','value']].values:
                g.text(x,y,f'{m:.0f}',color=color, fontsize=12)
           
        g.set_ylabel(''); g.grid(alpha=0.4, ls='-.')
        g.set_title(key)
        #g.legend(bbox_to_anchor=(1.01,0.8))
        g.legend(bbox_to_anchor=(1.,-0.2))
        pl.savefig(dir_name+'/'+key.replace(' ','_')+'.png', dpi=300, bbox_inches='tight')
        pl.show()
     