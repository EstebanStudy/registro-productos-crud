import pytest
import os
import json
from main import ProductoManager

# Configuración para tests
ARCHIVO_TEST = "test_productos.json"

@pytest.fixture
def manager():
    """Fixture que proporciona un manager limpio para cada test."""
    manager = ProductoManager(ARCHIVO_TEST)
    # Limpiar archivo de test antes de cada test
    if os.path.exists(ARCHIVO_TEST):
        os.remove(ARCHIVO_TEST)
    return manager

@pytest.fixture(autouse=True)
def cleanup_after_tests():
    """Limpia el archivo de test después de todos los tests."""
    yield
    if os.path.exists(ARCHIVO_TEST):
        os.remove(ARCHIVO_TEST)

class TestProductoManager:
    """Tests para la clase ProductoManager."""
    
    def test_crear_producto_exitoso(self, manager):
        """Test crear producto con datos válidos."""
        resultado = manager.crear_producto(1, "Lápiz HB", "Lápiz de grafito", 1500.0, 100)
        assert "✅ Producto 'Lápiz HB' agregado exitosamente (ID: 1)" in resultado
        
        # Verificar que se guardó correctamente
        producto = manager._obtener_producto_por_id(1)
        assert producto is not None
        assert producto["nombre"] == "Lápiz HB"
        assert producto["precio"] == 1500.0

    def test_crear_producto_id_duplicado(self, manager):
        """Test que no permite crear producto con ID duplicado."""
        manager.crear_producto(1, "Producto A", "Descripción A", 1000.0, 50)
        resultado = manager.crear_producto(1, "Producto B", "Descripción B", 2000.0, 60)
        
        assert "❌ El ID 1 ya existe" in resultado

    def test_crear_producto_datos_invalidos(self, manager):
        """Test validación de datos al crear producto."""
        # Nombre vacío
        resultado = manager.crear_producto(1, "", "Descripción", 1000.0, 50)
        assert "❌ El nombre debe ser un texto no vacío" in resultado
        
        # Precio negativo
        resultado = manager.crear_producto(2, "Producto", "Desc", -100.0, 50)
        assert "❌ El precio debe ser un número positivo" in resultado
        
        # Cantidad negativa
        resultado = manager.crear_producto(3, "Producto", "Desc", 1000.0, -10)
        assert "❌ La cantidad debe ser un número entero positivo" in resultado

    def test_leer_producto_existente(self, manager):
        """Test consultar producto existente."""
        manager.crear_producto(1, "Borrador", "Borrador blanco", 800.0, 150)
        resultado = manager.leer_producto(1)
        
        assert "🔍 Producto encontrado:" in resultado
        assert "Borrador" in resultado
        assert "800.00" in resultado
        assert "150" in resultado

    def test_leer_producto_no_existente(self, manager):
        """Test consultar producto que no existe."""
        resultado = manager.leer_producto(999)
        assert "❌ Producto con ID 999 no encontrado" in resultado

    def test_actualizar_producto_exitoso(self, manager):
        """Test actualizar producto existente."""
        manager.crear_producto(1, "Producto Original", "Desc original", 1000.0, 50)
        resultado = manager.actualizar_producto(1, "Producto Actualizado", "Nueva descripción", 2000.0, 75)
        
        assert "✏️ Producto 'Producto Actualizado' actualizado exitosamente (ID: 1)" in resultado
        
        # Verificar cambios
        producto = manager._obtener_producto_por_id(1)
        assert producto["nombre"] == "Producto Actualizado"
        assert producto["precio"] == 2000.0
        assert producto["cantidad"] == 75

    def test_actualizar_producto_no_existente(self, manager):
        """Test actualizar producto que no existe."""
        resultado = manager.actualizar_producto(999, "No existe", "Desc", 1000.0, 50)
        assert "❌ Producto con ID 999 no encontrado" in resultado

    def test_actualizar_producto_datos_invalidos(self, manager):
        """Test validación al actualizar producto."""
        manager.crear_producto(1, "Producto", "Desc", 1000.0, 50)
        
        # Precio negativo
        resultado = manager.actualizar_producto(1, "Producto", "Desc", -100.0, 50)
        assert "❌ El precio debe ser un número positivo" in resultado

    def test_eliminar_producto_exitoso(self, manager):
        """Test eliminar producto existente."""
        manager.crear_producto(1, "Producto a Eliminar", "Descripción", 1000.0, 50)
        resultado = manager.eliminar_producto(1)
        
        assert "🗑️ Producto 'Producto a Eliminar' eliminado exitosamente (ID: 1)" in resultado
        assert manager._obtener_producto_por_id(1) is None

    def test_eliminar_producto_no_existente(self, manager):
        """Test eliminar producto que no existe."""
        resultado = manager.eliminar_producto(999)
        assert "❌ Producto con ID 999 no encontrado" in resultado

    def test_listar_productos_vacio(self, manager):
        """Test listar cuando no hay productos."""
        resultado = manager.listar_productos()
        assert "📭 No hay productos registrados." in resultado

    def test_listar_productos_con_datos(self, manager):
        """Test listar cuando hay productos."""
        manager.crear_producto(1, "Producto A", "Desc A", 1000.0, 10)
        manager.crear_producto(2, "Producto B", "Desc B", 2000.0, 20)
        
        resultado = manager.listar_productos()
        
        assert "📋 Productos registrados:" in resultado
        assert "Producto A" in resultado
        assert "Producto B" in resultado
        assert "Valor total:" in resultado

    def test_buscar_por_nombre_encontrado(self, manager):
        """Test búsqueda por nombre que encuentra resultados."""
        manager.crear_producto(1, "Lápiz profesional", "Desc", 1500.0, 100)
        manager.crear_producto(2, "Borrador pequeño", "Desc", 800.0, 50)
        
        resultado = manager.buscar_por_nombre("profesional")
        
        assert "🔍 Resultados de búsqueda para 'profesional':" in resultado
        assert "Lápiz profesional" in resultado
        assert "Borrador pequeño" not in resultado

    def test_buscar_por_nombre_no_encontrado(self, manager):
        """Test búsqueda por nombre sin resultados."""
        manager.crear_producto(1, "Lápiz", "Desc", 1500.0, 100)
        
        resultado = manager.buscar_por_nombre("cuaderno")
        
        assert "🔍 No se encontraron productos con 'cuaderno' en el nombre" in resultado

    def test_buscar_por_nombre_case_insensitive(self, manager):
        """Test que la búsqueda es case insensitive."""
        manager.crear_producto(1, "LÁPIZ PROFESIONAL", "Desc", 1500.0, 100)
        
        resultado = manager.buscar_por_nombre("lápiz")
        
        assert "LÁPIZ PROFESIONAL" in resultado

    def test_obtener_estadisticas_vacio(self, manager):
        """Test estadísticas con inventario vacío."""
        resultado = manager.obtener_estadisticas()
        assert "📊 No hay productos para generar estadísticas" in resultado

    def test_obtener_estadisticas_con_datos(self, manager):
        """Test estadísticas con productos."""
        manager.crear_producto(1, "Producto A", "Desc A", 1000.0, 10)  # Valor: 10,000
        manager.crear_producto(2, "Producto B", "Desc B", 2000.0, 5)   # Valor: 10,000
        # Total: 20,000
        
        resultado = manager.obtener_estadisticas()
        
        assert "📊 Estadísticas del Inventario:" in resultado
        assert "Productos diferentes: 2" in resultado
        assert "Total de unidades: 15" in resultado
        assert "Valor total del inventario: $20,000.00" in resultado

    def test_producto_mas_caro_y_barato(self, manager):
        """Test identificación de producto más caro y más barato."""
        manager.crear_producto(1, "Barato", "Desc", 500.0, 10)
        manager.crear_producto(2, "Caro", "Desc", 5000.0, 5)
        manager.crear_producto(3, "Medio", "Desc", 2000.0, 8)
        
        resultado = manager.obtener_estadisticas()
        
        assert "Producto más caro: Caro ($5,000.00)" in resultado
        assert "Producto más barato: Barato ($500.00)" in resultado

    def test_validar_precio_decimal(self, manager):
        """Test que los precios decimales se redondean correctamente."""
        manager.crear_producto(1, "Producto", "Desc", 1234.567, 10)
        producto = manager._obtener_producto_por_id(1)
        
        assert producto["precio"] == 1234.57  # Redondeado a 2 decimales

class TestIntegracion:
    """Tests de integración que simulan flujos completos."""
    
    def test_flujo_completo_crud(self, manager):
        """Test que simula un flujo completo de operaciones CRUD."""
        # Create
        resultado_crear = manager.crear_producto(1, "Producto Test", "Descripción test", 1000.0, 50)
        assert "agregado exitosamente" in resultado_crear.lower()
        
        # Read
        resultado_leer = manager.leer_producto(1)
        assert "Producto Test" in resultado_leer
        
        # Update
        resultado_actualizar = manager.actualizar_producto(1, "Producto Modificado", "Nueva desc", 2000.0, 75)
        assert "actualizado exitosamente" in resultado_actualizar.lower()
        
        # Verify update
        producto = manager._obtener_producto_por_id(1)
        assert producto["nombre"] == "Producto Modificado"
        assert producto["precio"] == 2000.0
        
        # Delete
        resultado_eliminar = manager.eliminar_producto(1)
        assert "eliminado exitosamente" in resultado_eliminar.lower()
        
        # Verify delete
        assert manager._obtener_producto_por_id(1) is None

    def test_multiples_operaciones_consistencia(self, manager):
        """Test que verifica consistencia después de múltiples operaciones."""
        # Crear varios productos
        for i in range(1, 6):
            manager.crear_producto(i, f"Producto {i}", f"Desc {i}", i * 1000.0, i * 10)
        
        # Verificar que todos existen
        for i in range(1, 6):
            assert manager._obtener_producto_por_id(i) is not None
        
        # Eliminar algunos
        manager.eliminar_producto(2)
        manager.eliminar_producto(4)
        
        # Verificar estado final
        assert manager._obtener_producto_por_id(1) is not None
        assert manager._obtener_producto_por_id(2) is None
        assert manager._obtener_producto_por_id(3) is not None
        assert manager._obtener_producto_por_id(4) is None
        assert manager._obtener_producto_por_id(5) is not None
        
        # Listar debería mostrar solo los existentes
        resultado = manager.listar_productos()
        assert "Producto 1" in resultado
        assert "Producto 2" not in resultado
        assert "Producto 3" in resultado
        assert "Producto 4" not in resultado
        assert "Producto 5" in resultado

def test_archivo_persistencia(manager):
    """Test que verifica la persistencia en archivo."""
    # Crear producto
    manager.crear_producto(1, "Producto Persistente", "Desc", 1000.0, 50)
    
    # Crear nuevo manager (simula reinicio de aplicación)
    nuevo_manager = ProductoManager(ARCHIVO_TEST)
    
    # Verificar que el producto persiste
    producto = nuevo_manager._obtener_producto_por_id(1)
    assert producto is not None
    assert producto["nombre"] == "Producto Persistente"

if __name__ == "__main__":
    # Ejecutar tests manualmente
    pytest.main([__file__, "-v"])