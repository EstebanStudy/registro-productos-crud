import json
import os
from typing import List, Dict, Any, Optional

ARCHIVO = "productos.json"

class ProductoManager:
    """Sistema de gestión de productos con operaciones CRUD completas."""
    
    def __init__(self, archivo: str = ARCHIVO):
        self.archivo = archivo
    
    def _cargar_productos(self) -> List[Dict[str, Any]]:
        """Carga los productos desde el archivo JSON."""
        try:
            if not os.path.exists(self.archivo):
                return []
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error cargando productos: {e}")
            return []
    
    def _guardar_productos(self, productos: List[Dict[str, Any]]) -> bool:
        """Guarda los productos en el archivo JSON."""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(productos, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"⚠️ Error guardando productos: {e}")
            return False
    
    def _validar_datos_producto(self, nombre: str, descripcion: str, precio: float, cantidad: int) -> bool:
        """Valida los datos del producto antes de guardar."""
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) == 0:
            raise ValueError("El nombre debe ser un texto no vacío")
        
        if not isinstance(descripcion, str):
            raise ValueError("La descripción debe ser un texto")
        
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número positivo")
        
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero positivo")
        
        return True
    
    def _producto_existe(self, id: int) -> bool:
        """Verifica si un producto con el ID dado existe."""
        productos = self._cargar_productos()
        return any(p["id"] == id for p in productos)
    
    def _obtener_producto_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un producto por su ID."""
        productos = self._cargar_productos()
        for producto in productos:
            if producto["id"] == id:
                return producto
        return None

    # ===================== OPERACIONES CRUD =====================

    def crear_producto(self, id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
        """Crea un nuevo producto con validaciones."""
        try:
            # Validaciones
            if self._producto_existe(id):
                raise KeyError(f"El ID {id} ya existe")
            
            self._validar_datos_producto(nombre, descripcion, precio, cantidad)
            
            # Crear producto
            productos = self._cargar_productos()
            nuevo_producto = {
                "id": id,
                "nombre": nombre.strip(),
                "descripcion": descripcion.strip(),
                "precio": round(float(precio), 2),
                "cantidad": cantidad
            }
            
            productos.append(nuevo_producto)
            
            if self._guardar_productos(productos):
                return f"✅ Producto '{nombre}' agregado exitosamente (ID: {id})"
            else:
                return "❌ Error al guardar el producto"
                
        except (KeyError, ValueError) as e:
            return f"❌ {str(e)}"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

    def leer_producto(self, id: int) -> str:
        """Consulta un producto por su ID."""
        try:
            producto = self._obtener_producto_por_id(id)
            if producto:
                return (f"🔍 Producto encontrado:\n"
                        f"   • ID: {producto['id']}\n"
                        f"   • Nombre: {producto['nombre']}\n"
                        f"   • Descripción: {producto['descripcion']}\n"
                        f"   • Precio: ${producto['precio']:,.2f}\n"
                        f"   • Cantidad: {producto['cantidad']} unidades")
            else:
                raise KeyError(f"Producto con ID {id} no encontrado")
                
        except KeyError as e:
            return f"❌ {str(e)}"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

    def actualizar_producto(self, id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
        """Actualiza un producto existente."""
        try:
            # Validaciones
            if not self._producto_existe(id):
                raise KeyError(f"Producto con ID {id} no encontrado")
            
            self._validar_datos_producto(nombre, descripcion, precio, cantidad)
            
            # Actualizar producto
            productos = self._cargar_productos()
            for producto in productos:
                if producto["id"] == id:
                    producto.update({
                        "nombre": nombre.strip(),
                        "descripcion": descripcion.strip(),
                        "precio": round(float(precio), 2),
                        "cantidad": cantidad
                    })
                    break
            
            if self._guardar_productos(productos):
                return f"✏️ Producto '{nombre}' actualizado exitosamente (ID: {id})"
            else:
                return "❌ Error al guardar los cambios"
                
        except (KeyError, ValueError) as e:
            return f"❌ {str(e)}"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

    def eliminar_producto(self, id: int) -> str:
        """Elimina un producto por su ID."""
        try:
            productos = self._cargar_productos()
            producto_encontrado = None
            
            for i, producto in enumerate(productos):
                if producto["id"] == id:
                    producto_encontrado = producto
                    productos.pop(i)
                    break
            
            if not producto_encontrado:
                raise KeyError(f"Producto con ID {id} no encontrado")
            
            if self._guardar_productos(productos):
                return f"🗑️ Producto '{producto_encontrado['nombre']}' eliminado exitosamente (ID: {id})"
            else:
                return "❌ Error al guardar los cambios"
                
        except KeyError as e:
            return f"❌ {str(e)}"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"

    def listar_productos(self) -> str:
        """Lista todos los productos registrados."""
        try:
            productos = self._cargar_productos()
            
            if not productos:
                return "📭 No hay productos registrados."
            
            resultado = ["📋 Productos registrados:"]
            total_valor = 0
            
            for producto in productos:
                valor_total = producto['precio'] * producto['cantidad']
                total_valor += valor_total
                
                resultado.append(
                    f"   • ID: {producto['id']} | "
                    f"Nombre: {producto['nombre']} | "
                    f"Precio: ${producto['precio']:,.2f} | "
                    f"Cantidad: {producto['cantidad']} | "
                    f"Valor total: ${valor_total:,.2f}"
                )
            
            resultado.append(f"\n💰 Valor total del inventario: ${total_valor:,.2f}")
            resultado.append(f"📊 Total de productos diferentes: {len(productos)}")
            
            return "\n".join(resultado)
            
        except Exception as e:
            return f"❌ Error al listar productos: {str(e)}"

    def buscar_por_nombre(self, nombre: str) -> str:
        """Busca productos por nombre (búsqueda parcial)."""
        try:
            productos = self._cargar_productos()
            resultados = [p for p in productos if nombre.lower() in p['nombre'].lower()]
            
            if not resultados:
                return f"🔍 No se encontraron productos con '{nombre}' en el nombre"
            
            resultado = [f"🔍 Resultados de búsqueda para '{nombre}':"]
            for producto in resultados:
                resultado.append(
                    f"   • ID: {producto['id']} | "
                    f"Nombre: {producto['nombre']} | "
                    f"Precio: ${producto['precio']:,.2f} | "
                    f"Cantidad: {producto['cantidad']}"
                )
            
            return "\n".join(resultado)
            
        except Exception as e:
            return f"❌ Error en la búsqueda: {str(e)}"

    def obtener_estadisticas(self) -> str:
        """Muestra estadísticas del inventario."""
        try:
            productos = self._cargar_productos()
            
            if not productos:
                return "📊 No hay productos para generar estadísticas"
            
            total_productos = sum(p['cantidad'] for p in productos)
            valor_total = sum(p['precio'] * p['cantidad'] for p in productos)
            precio_promedio = valor_total / total_productos if total_productos > 0 else 0
            producto_mas_caro = max(productos, key=lambda x: x['precio'])
            producto_mas_barato = min(productos, key=lambda x: x['precio'])
            
            return (
                f"📊 Estadísticas del Inventario:\n"
                f"   • Productos diferentes: {len(productos)}\n"
                f"   • Total de unidades: {total_productos}\n"
                f"   • Valor total del inventario: ${valor_total:,.2f}\n"
                f"   • Precio promedio por unidad: ${precio_promedio:,.2f}\n"
                f"   • Producto más caro: {producto_mas_caro['nombre']} (${producto_mas_caro['precio']:,.2f})\n"
                f"   • Producto más barato: {producto_mas_barato['nombre']} (${producto_mas_barato['precio']:,.2f})"
            )
            
        except Exception as e:
            return f"❌ Error generando estadísticas: {str(e)}"
    
    def agregar(self, id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
        return self.crear_producto(id, nombre, descripcion, precio, cantidad)
    
    def consultar(self, id: int) -> str:
        try:
            producto = self._obtener_producto_por_id(id)
            if producto:
                return (f"Consultado: {id} -> {producto['nombre']} | "
                    f"{producto['descripcion']} | "
                    f"Precio: {producto['precio']} | "
                    f"Cantidad: {producto['cantidad']}")
            else:
                return "Clave no encontrada"
        except Exception:
            return "Clave no encontrada"
    
    def modificar(self, id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
        try:
            if not self._producto_existe(id):
                return "Clave no encontrada"
            
            # Validación básica para compatibilidad
            if not nombre or precio < 0 or cantidad < 0:
                return "Clave no encontrada"
            
            productos = self._cargar_productos()
            for producto in productos:
                if producto["id"] == id:
                    producto.update({
                        "nombre": nombre,
                        "descripcion": descripcion,
                        "precio": precio,
                        "cantidad": cantidad
                    })
                    break
            
            if self._guardar_productos(productos):
                return f"Modificado: {id} -> {nombre}"
            else:
                return "Clave no encontrada"
                
        except Exception:
            return "Clave no encontrada"
    
    def eliminar(self, id: int) -> str:
        try:
            productos = self._cargar_productos()
            for i, producto in enumerate(productos):
                if producto["id"] == id:
                    productos.pop(i)
                    self._guardar_productos(productos)
                    return f"Eliminado: {id}"
            return "Clave no encontrada"
        except Exception:
            return "Clave no encontrada"

# ===================== FUNCIONES GLOBALES PARA COMPATIBILIDAD =====================

_manager_global = ProductoManager()

def agregar(id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
    return _manager_global.agregar(id, nombre, descripcion, precio, cantidad)

def consultar(id: int) -> str:
    return _manager_global.consultar(id)

def modificar(id: int, nombre: str, descripcion: str, precio: float, cantidad: int) -> str:
    return _manager_global.modificar(id, nombre, descripcion, precio, cantidad)

def eliminar(id: int) -> str:
    return _manager_global.eliminar(id)

def demostrar_sistema():
    """Demuestra todas las funcionalidades del sistema."""
    manager = ProductoManager()
    
    print("=== 🛍️ SISTEMA DE GESTIÓN DE PRODUCTOS ===\n")
    
    # Crear productos
    print("1. CREANDO PRODUCTOS:")
    print(manager.crear_producto(1, "Lápiz HB", "Lápiz de grafito calidad premium", 1500.0, 200))
    print(manager.crear_producto(2, "Borrador", "Borrador blanco no tóxico", 800.0, 150))
    print(manager.crear_producto(3, "Cuaderno profesional", "100 hojas rayadas", 12500.0, 50))
    
    # Intentar crear producto con ID duplicado
    print("\n2. INTENTO DE CREAR PRODUCTO DUPLICADO:")
    print(manager.crear_producto(1, "Producto duplicado", "Esto debería fallar", 1000.0, 100))
    
    # Listar productos
    print("\n3. LISTADO COMPLETO:")
    print(manager.listar_productos())
    
    # Consultar producto
    print("\n4. CONSULTANDO PRODUCTO:")
    print(manager.leer_producto(2))
    
    # Actualizar producto
    print("\n5. ACTUALIZANDO PRODUCTO:")
    print(manager.actualizar_producto(1, "Lápiz profesional HB", "Para dibujo técnico y artístico", 3500.0, 80))
    
    # Buscar productos
    print("\n6. BUSCANDO PRODUCTOS:")
    print(manager.buscar_por_nombre("profesional"))
    
    # Mostrar estadísticas
    print("\n7. ESTADÍSTICAS:")
    print(manager.obtener_estadisticas())
    
    # Eliminar producto
    print("\n8. ELIMINANDO PRODUCTO:")
    print(manager.eliminar_producto(2))
    
    # Listar después de eliminar
    print("\n9. ESTADO FINAL:")
    print(manager.listar_productos())
    
    # Demo de compatibilidad con funciones globales
    print("\n10. COMPATIBILIDAD CON FUNCIONES GLOBALES:")
    print(agregar(99, "Producto Test", "Para testing", 999.0, 10))
    print(consultar(99))
    print(modificar(99, "Producto Modificado", "Desc modificada", 1111.0, 5))
    print(eliminar(99))

if __name__ == "__main__":
    demostrar_sistema()