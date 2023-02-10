from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
    # настройте сериализатор для продукта
    # pass


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']
    # настройте сериализатор для позиции продукта на складе
    # pass


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']
    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for pos in positions:
            # StockProduct.objects.create(stock=stock, product=pos['product'], quantity=pos['quantity'], price=pos['price'])
            # StockProduct.objects.create(stock=stock,
            #     product=pos.get('product'),
            #     quantity=pos.get('quantity'),
            #     price=pos.get('price'))
            StockProduct.objects.create(stock=stock, **pos)
        # создаем склад по его параметрам
        # stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # product = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for pos in positions:
            product = pos.get('product')              
            quantity = pos.get('quantity')
            price = pos.get('price')
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={'price':price, 'quantity':quantity}
            )        

        return stock
