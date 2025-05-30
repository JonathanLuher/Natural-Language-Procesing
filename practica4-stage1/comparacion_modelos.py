import os
import pandas as pd
from glob import glob

def generar_tabla_consolidada():
    try:
        # Configuración inicial
        output_path = os.path.join('corpus', 'comparacion_final.xlsx')
        os.makedirs('corpus', exist_ok=True)
        
        mejores_modelos = []
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for norm_num in range(1, 6):
                model_folder = os.path.join('corpus', f'normalizacion{norm_num}', 'Modelos')
                
                # Verificar si existe la carpeta
                if not os.path.exists(model_folder):
                    print(f"¡Advertencia! No se encontró la carpeta: {model_folder}")
                    continue
                
                reportes = glob(os.path.join(model_folder, '*_report.csv'))
                
                if not reportes:
                    print(f"¡Advertencia! No hay reportes en: {model_folder}")
                    continue
                
                df_resultados = pd.DataFrame()
                
                for reporte in reportes:
                    try:
                        nombre = os.path.basename(reporte).replace('_report.csv', '')
                        partes = nombre.split('_')
                        rep = '_'.join(partes[:-1])
                        modelo = partes[-1]
                        
                        df_reporte = pd.read_csv(reporte, index_col=0)
                        f1_macro = df_reporte.loc['macro avg', 'f1-score']
                        df_resultados.loc[rep, modelo] = f1_macro
                    
                    except Exception as e:
                        print(f"Error procesando {reporte}: {str(e)}")
                        continue
                
                if not df_resultados.empty:
                    # Encontrar el mejor modelo
                    mejor_fila, mejor_col = df_resultados.stack().idxmax()
                    mejor_score = df_resultados.loc[mejor_fila, mejor_col]
                    mejores_modelos.append({
                        'Normalización': norm_num,
                        'Representación': mejor_fila,
                        'Modelo': mejor_col,
                        'F1-Score': f"{mejor_score:.4f}"
                    })
                    
                    # Guardar en Excel
                    df_resultados.to_excel(writer, sheet_name=f'Norm{norm_num}')
            
            # Guardar resumen de mejores modelos
            if mejores_modelos:
                pd.DataFrame(mejores_modelos).to_excel(
                    writer, 
                    sheet_name='RESUMEN',
                    index=False
                )
        
        # Mostrar resultados en consola
        if mejores_modelos:
            print("\n═"*50)
            print("MEJORES MODELOS POR NORMALIZACIÓN")
            print("═"*50)
            for res in mejores_modelos:
                print(f"Norm {res['Normalización']}:")
                print(f"• Representación: {res['Representación']}")
                print(f"• Modelo: {res['Modelo']}")
                print(f"• F1-Score: {res['F1-Score']}")
                print("─"*50)
            
            print(f"\n✔ Tabla consolidada guardada en: {output_path}")
        else:
            print("No se encontraron resultados válidos para generar el reporte.")
    
    except Exception as e:
        print(f"\n✖ Error inesperado: {str(e)}")

if __name__ == "__main__":
    generar_tabla_consolidada()