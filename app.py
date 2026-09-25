import streamlit as st
import numpy as np
import pandas as pd
from libreria_funciones_proyecto1 import calcular_depreciacion_linea_recta
from librería_clases_proyecto1 import InventarioProducto

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================
st.set_page_config(page_title="Proyecto 1 - Python Fundamentals", layout="centered")

# ==========================================================
# MENÚ LATERAL
# ==========================================================
menu = st.sidebar.selectbox(
    "Selecciona una sección",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# ==========================================================
# HOME
# ==========================================================
if menu == "Home":
    st.title("Proyecto Aplicado en Streamlit")
    st.subheader("Fundamentos de Programación - Python for Analytics")

    st.image("logo-secundario-dmc-institute-01.png", width=200)

    st.markdown("**Nombre del estudiante:** Alexander Marcel José Ñaccha Ñarquez")
    st.markdown("**Módulo:** Módulo 1 - Python Fundamentals")
    st.markdown("**Año:** 2026")

    st.write("")
    st.markdown("### Descripción del proyecto")
    st.write(
        "Esta aplicación fue desarrollada como Proyecto 1 de la Especialización en "
        "Python for Analytics. Integra los conceptos aprendidos durante el Módulo 1: "
        "variables, estructuras de datos, control de flujo, funciones, programación "
        "funcional y programación orientada a objetos (POO)."
    )

    st.markdown("### Tecnologías utilizadas")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- NumPy")
    st.write("- Pandas")

# ==========================================================
# EJERCICIO 1 - FLUJO DE CAJA CON LISTAS
# ==========================================================
elif menu == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de caja con listas")

    st.markdown(
        "En este ejercicio se registran movimientos financieros (ingresos y gastos) "
        "en una lista. Al final se calcula el total de ingresos, el total de gastos "
        "y el saldo final del flujo de caja."
    )

    # Lista vacía para guardar los movimientos (se conserva con session_state)
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []

    concepto = st.text_input("Concepto del movimiento")
    tipo_movimiento = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
    valor = st.number_input("Valor", min_value=0.0, step=1.0)

    if st.button("Agregar movimiento"):
        if concepto == "":
            st.error("Debes ingresar un concepto")
        else:
            st.session_state.movimientos.append({
                "Concepto": concepto,
                "Tipo": tipo_movimiento,
                "Valor": valor
            })
            st.success("Movimiento agregado")

    if len(st.session_state.movimientos) > 0:
        df_movimientos = pd.DataFrame(st.session_state.movimientos)
        st.markdown("### Movimientos registrados")
        st.dataframe(df_movimientos)

        total_ingresos = df_movimientos[df_movimientos["Tipo"] == "Ingreso"]["Valor"].sum()
        total_gastos = df_movimientos[df_movimientos["Tipo"] == "Gasto"]["Valor"].sum()
        saldo_final = total_ingresos - total_gastos

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"${total_ingresos:.2f}")
        col2.metric("Total Gastos", f"${total_gastos:.2f}")
        col3.metric("Saldo Final", f"${saldo_final:.2f}")

        if saldo_final >= 0:
            st.success("El flujo de caja está a favor")
        else:
            st.error("El flujo de caja está en contra")
    else:
        st.write("Aún no se han registrado movimientos.")

# ==========================================================
# EJERCICIO 2 - REGISTRO CON NUMPY, ARRAYS Y DATAFRAME
# ==========================================================
elif menu == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro con NumPy, arrays y DataFrame")

    st.markdown(
        "En este ejercicio se registran productos usando **arreglos de NumPy**. "
        "Cada vez que se agrega un producto, la información se guarda en un array "
        "y luego se convierte en un DataFrame que se muestra actualizado en pantalla."
    )

    if "productos" not in st.session_state:
        st.session_state.productos = np.empty((0, 4))
        st.session_state.nombres_productos = []
        st.session_state.categorias_productos = []

    nombre_producto = st.text_input("Nombre del producto")
    categoria = st.selectbox("Categoría", ["Alimentos", "Limpieza", "Electrónica", "Otros"])
    precio = st.number_input("Precio", min_value=0.0, step=0.5)
    cantidad = st.number_input("Cantidad", min_value=0, step=1)

    if st.button("Agregar registro"):
        if nombre_producto == "":
            st.error("Debes ingresar el nombre del producto")
        else:
            total = precio * cantidad

            nuevo_registro = np.array([[precio, cantidad, total, 0]])
            st.session_state.productos = np.vstack([st.session_state.productos, nuevo_registro])
            st.session_state.nombres_productos.append(nombre_producto)
            st.session_state.categorias_productos.append(categoria)

            st.success("Registro agregado")

    if len(st.session_state.nombres_productos) > 0:
        df_productos = pd.DataFrame({
            "Producto": st.session_state.nombres_productos,
            "Categoría": st.session_state.categorias_productos,
            "Precio": st.session_state.productos[:, 0],
            "Cantidad": st.session_state.productos[:, 1],
            "Total": st.session_state.productos[:, 2]
        })

        st.markdown("### Registros (DataFrame)")
        st.dataframe(df_productos)
    else:
        st.write("Aún no se han registrado productos.")

# ==========================================================
# EJERCICIO 3 - USO DE FUNCIÓN DESDE LIBRERÍA EXTERNA
# ==========================================================
elif menu == "Ejercicio 3":
    st.title("Ejercicio 3 - Uso de función desde una librería externa")

    st.markdown(
        "Para este ejercicio se seleccionó la función **calcular_depreciacion_linea_recta**, "
        "de la librería `libreria_funciones_proyecto1.py`, relacionada con el área "
        "de Contabilidad. Esta función calcula la depreciación anual y mensual de "
        "un activo fijo usando el método de línea recta."
    )

    st.markdown(
        "La categoría del activo define la **tasa máxima anual de depreciación** "
        "aceptada por SUNAT (Art. 22 del Reglamento de la Ley del Impuesto a la Renta). "
        "Con esa tasa se calcula la vida útil en años que se envía a la función."
    )

    st.selectbox("Función seleccionada", ["calcular_depreciacion_linea_recta"])

    # Tasas máximas anuales de depreciación según SUNAT
    tasas_sunat = {
        "Edificios y construcciones": 5,
        "Ganado de trabajo y reproducción, redes de pesca": 25,
        "Vehículos de transporte terrestre (excepto ferrocarriles), hornos en general": 20,
        "Maquinaria y equipo (minería, petróleo, construcción)": 20,
        "Equipos de procesamiento de datos": 25,
        "Maquinaria y equipo adquirido desde el 01.01.1991": 10,
        "Otros bienes del activo fijo": 10
    }

    categoria = st.selectbox("Categoría del activo (SUNAT)", list(tasas_sunat.keys()))
    tasa_maxima = tasas_sunat[categoria]
    vida_util = round(100 / tasa_maxima)

    st.markdown(f"**Tasa máxima anual SUNAT:** {tasa_maxima}%  |  **Vida útil resultante:** {vida_util} años")

    costo_activo = st.number_input("Costo del activo (S/)", min_value=0.0, step=100.0)
    valor_residual = st.number_input("Valor residual (S/)", min_value=0.0, step=50.0)

    if "historico_depreciacion" not in st.session_state:
        st.session_state.historico_depreciacion = []

    if st.button("Calcular depreciación"):
        try:
            resultado = calcular_depreciacion_linea_recta(costo_activo, valor_residual, vida_util)

            st.write("Depreciación anual: S/", resultado["depreciacion_anual"])
            st.write("Depreciación mensual: S/", resultado["depreciacion_mensual"])

            st.session_state.historico_depreciacion.append({
                "Categoría SUNAT": categoria,
                "Tasa anual SUNAT": f"{tasa_maxima}%",
                "Costo activo (S/)": costo_activo,
                "Valor residual (S/)": valor_residual,
                "Vida útil (años)": vida_util,
                "Depreciación anual (S/)": resultado["depreciacion_anual"],
                "Depreciación mensual (S/)": resultado["depreciacion_mensual"]
            })

        except ValueError as e:
            st.error(f"Error: {e}")

    if len(st.session_state.historico_depreciacion) > 0:
        st.markdown("### Histórico de resultados")
        df_historico = pd.DataFrame(st.session_state.historico_depreciacion)
        st.dataframe(df_historico)

# ==========================================================
# EJERCICIO 4 - USO DE CLASE DESDE LIBRERÍA EXTERNA CON CRUD
# ==========================================================
elif menu == "Ejercicio 4":
    st.title("Ejercicio 4 - Uso de clases desde una librería externa con CRUD")

    st.markdown(
        "Para este ejercicio se seleccionó la clase **InventarioProducto**, de la "
        "librería `librería_clases_proyecto1.py`, relacionada con el área de "
        "Contabilidad / Inventario. Permite crear, leer, actualizar y eliminar "
        "productos del inventario."
    )

    # Diccionario en session_state para guardar los objetos InventarioProducto
    if "inventario" not in st.session_state:
        st.session_state.inventario = {}

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["Crear", "Leer", "Actualizar", "Eliminar"]
    )

    # ------------------ CREAR ------------------
    with tab_crear:
        st.subheader("Crear producto")

        nombre = st.text_input("Nombre del producto", key="crear_nombre")
        costo_unitario = st.number_input("Costo unitario ($)", min_value=0.01, step=0.5, key="crear_costo")
        precio_unitario = st.number_input("Precio unitario ($)", min_value=0.01, step=0.5, key="crear_precio")
        stock_actual = st.number_input("Stock actual", min_value=0, step=1, key="crear_stock_actual")
        stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1, key="crear_stock_minimo")

        if st.button("Crear producto"):
            if nombre == "":
                st.error("Debes ingresar el nombre del producto")
            elif nombre in st.session_state.inventario:
                st.error("Ya existe un producto con ese nombre")
            else:
                try:
                    producto = InventarioProducto(
                        nombre, costo_unitario, precio_unitario, stock_actual, stock_minimo
                    )
                    st.session_state.inventario[nombre] = producto
                    st.success(f"Producto '{nombre}' creado correctamente")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # ------------------ LEER ------------------
    with tab_leer:
        st.subheader("Productos registrados")

        if len(st.session_state.inventario) > 0:
            resumenes = [p.resumen() for p in st.session_state.inventario.values()]
            df_inventario = pd.DataFrame(resumenes)
            st.dataframe(df_inventario)
        else:
            st.write("Aún no se han registrado productos.")

    # ------------------ ACTUALIZAR ------------------
    with tab_actualizar:
        st.subheader("Actualizar producto")

        if len(st.session_state.inventario) > 0:
            producto_actualizar = st.selectbox(
                "Selecciona el producto a actualizar",
                list(st.session_state.inventario.keys()),
                key="actualizar_select"
            )

            nuevo_precio = st.number_input("Nuevo precio unitario ($)", min_value=0.01, step=0.5, key="actualizar_precio")
            nuevo_stock = st.number_input("Nuevo stock actual", min_value=0, step=1, key="actualizar_stock")

            if st.button("Actualizar producto"):
                st.session_state.inventario[producto_actualizar].precio_unitario = nuevo_precio
                st.session_state.inventario[producto_actualizar].stock_actual = nuevo_stock
                st.success(f"Producto '{producto_actualizar}' actualizado correctamente")

                st.markdown("**Resumen actualizado:**")
                st.write(st.session_state.inventario[producto_actualizar].resumen())
        else:
            st.write("Aún no se han registrado productos.")

    # ------------------ ELIMINAR ------------------
    with tab_eliminar:
        st.subheader("Eliminar producto")

        if len(st.session_state.inventario) > 0:
            producto_eliminar = st.selectbox(
                "Selecciona el producto a eliminar",
                list(st.session_state.inventario.keys()),
                key="eliminar_select"
            )

            if st.button("Eliminar producto"):
                del st.session_state.inventario[producto_eliminar]
                st.success(f"Producto '{producto_eliminar}' eliminado correctamente")
        else:
            st.write("Aún no se han registrado productos.")
