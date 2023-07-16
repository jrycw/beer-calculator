import asyncio

import streamlit as st

st.set_page_config('Beer Calculator',  layout='centered')


class BeerCalculator:
    def __init__(self,
                 money,
                 caps=0,
                 bottles=0,
                 *,
                 unit_beer_price=2,
                 cap_to_beer_ratio=4,
                 bottle_to_beer_ratio=2):
        self.money = money
        self.caps = caps
        self.bottles = bottles
        self.total_bottles = self.bottles

        self.unit_beer_price = unit_beer_price
        self.cap_to_beer_ratio = cap_to_beer_ratio
        self.bottle_to_beer_ratio = bottle_to_beer_ratio

        self.rounds = 1

    async def exchange(self):
        while True:
            await self.buy_beer()
            await self.cap_to_beer()
            await self.bottle_to_beer()
            if self.caps < self.cap_to_beer_ratio and self.bottles < self.bottle_to_beer_ratio:
                break
            self.rounds += 1

    async def buy_beer(self):
        if self.money >= self.unit_beer_price:
            m, r = divmod(self.money, self.unit_beer_price)
            self.money = r
            self.bottles += m
            self.caps += m
            self.total_bottles += m

    async def cap_to_beer(self):
        if self.caps >= self.cap_to_beer_ratio:
            m, r = divmod(self.caps, self.cap_to_beer_ratio)
            self.caps = m + r
            self.bottles += m
            self.total_bottles += m

    async def bottle_to_beer(self):
        if self.bottles >= self.bottle_to_beer_ratio:
            m, r = divmod(self.bottles, self.bottle_to_beer_ratio)
            self.bottles = m + r
            self.caps += m
            self.total_bottles += m

    @property
    def status(self):
        return [f'total_beers: {self.total_bottles}',
                f'caps: {self.caps}',
                f'bottles: {self.bottles}']

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}({', '.join(self.status)})"


async def main():
    st.header('啤酒兌換計算機')
    caps, bottles = 0, 0

    with st.form('beer-exchange-form'):
        money = st.slider('Money: ', min_value=0, value=10, step=1)
        unit_beer_price = st.slider('啤酒每瓶售價: ', min_value=1, value=2)
        cap_to_beer_ratio = st.slider('幾個瓶蓋換一瓶啤酒: ', min_value=2, value=4)
        bottle_to_beer_ratio = st.slider('幾個空瓶換一瓶啤酒: ', min_value=2, value=2)
        submitted = st.form_submit_button('計算')
        if submitted:
            bc = BeerCalculator(money, caps, bottles,
                                unit_beer_price=unit_beer_price,
                                cap_to_beer_ratio=cap_to_beer_ratio,
                                bottle_to_beer_ratio=bottle_to_beer_ratio)
            await bc.exchange()
            st.write(
                f'總共可以喝{bc.total_bottles}瓶啤酒, 剩下{bc.caps}個瓶蓋及{bc.bottles}個空瓶。')


if __name__ == '__main__':
    asyncio.run(main())
