#!/usr/bin/env python3
"""
J.A.R.V.I.S Trading & Broker Skills Backend
Provides market data, technical analysis, portfolio tracking,
risk management, trade execution, and broker integrations.
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    SL = "sl"
    SL_LIMIT = "sl_limit"


class OrderStatus(Enum):
    PENDING = "pending"
    OPEN = "open"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Position:
    symbol: str
    quantity: float
    average_price: float
    current_price: float = 0.0
    side: str = "long"
    product: str = "intraday"


@dataclass
class Order:
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Trade:
    trade_id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    fees: float = 0.0
    tax: float = 0.0


@dataclass
class PortfolioSnapshot:
    timestamp: datetime
    cash: float
    holdings_value: float
    total_value: float
    realized_pnl: float
    unrealized_pnl: float


def _generate_id(prefix: str) -> str:
    raw = f"{prefix}-{datetime.now().isoformat()}-{time.time()}"
    return hashlib.sha1(raw.encode()).hexdigest()[:10]


def _make_candles(symbol: str, base_price: float = 100.0, count: int = 200) -> List[Candle]:
    now = datetime.now()
    candles: List[Candle] = []
    price = base_price
    for i in range(count):
        ts = now - timedelta(minutes=(count - i))
        drift = (hash(f"{symbol}-{ts.minute}") % 100) / 1000.0
        up = ((hash(f"{symbol}-open-{ts.minute}") % 200) - 100) / 1000.0
        o = price
        c = max(0.5, price + drift + up)
        h = max(o, c) + abs((hash(f"{symbol}-high-{ts.minute}") % 100)) / 1000.0
        l = min(o, c) - abs((hash(f"{symbol}-low-{ts.minute}") % 100)) / 1000.0
        v = max(100, (hash(f"{symbol}-vol-{ts.minute}") % 10000))
        candles.append(Candle(timestamp=ts, open=o, high=h, low=l, close=c, volume=float(v)))
        price = c
    return candles


class MarketDataEngine:
    """Market data and technical analysis engine."""

    def __init__(self):
        self.candles: Dict[str, List[Candle]] = {}
        self.quotes: Dict[str, Dict] = {}
        self._seed_market()

    def _seed_market(self):
        symbols = [
            "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
            "BTCUSD", "ETHUSD", "SOLUSD",
            "EURUSD", "GBPUSD", "USDJPY",
            "GOLD", "SILVER", "CRUDE",
        ]
        for symbol in symbols:
            base = 100.0 if "USD" not in symbol else 1.0
            if symbol in {"BTCUSD", "ETHUSD", "SOLUSD"}:
                base = 30000.0 if symbol == "BTCUSD" else 1800.0 if symbol == "ETHUSD" else 120.0
            elif symbol in {"EURUSD", "GBPUSD", "USDJPY"}:
                base = 1.08 if symbol == "EURUSD" else 1.27 if symbol == "GBPUSD" else 149.5
            elif symbol in {"GOLD", "SILVER", "CRUDE"}:
                base = 2300.0 if symbol == "GOLD" else 27.5 if symbol == "SILVER" else 72.0
            elif "BANK" in symbol:
                base = 900.0
            else:
                base = 2500.0
            self.candles[symbol] = _make_candles(symbol, base_price=base, count=300)
            self.quotes[symbol] = self._quote_from_candles(self.candles[symbol])

    def _quote_from_candles(self, candles: List[Candle]) -> Dict:
        last = candles[-1]
        prev = candles[-2]
        change = last.close - prev.close
        pct = (change / prev.close) * 100 if prev.close else 0.0
        return {
            "symbol": None,
            "price": round(last.close, 4),
            "change": round(change, 4),
            "change_percent": round(pct, 3),
            "open": round(last.open, 4),
            "high": round(last.high, 4),
            "low": round(last.low, 4),
            "volume": int(last.volume),
            "timestamp": last.timestamp.isoformat(),
        }

    def get_quote(self, symbol: str) -> Optional[Dict]:
        if symbol not in self.candles:
            return None
        quote = dict(self.quotes[symbol])
        quote["symbol"] = symbol
        quote["ltp"] = quote["price"]
        return quote

    def get_quotes(self, symbols: List[str]) -> List[Dict]:
        results = []
        for symbol in symbols:
            quote = self.get_quote(symbol)
            if quote:
                results.append(quote)
        return results

    def get_candles(self, symbol: str, count: int = 100) -> List[Dict]:
        if symbol not in self.candles:
            return []
        data = self.candles[symbol][-count:]
        return [
            {
                "timestamp": c.timestamp.isoformat(),
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            }
            for c in data
        ]

    def technical_analysis(self, symbol: str) -> Dict:
        closes = [c.close for c in self.candles.get(symbol, [])]
        if len(closes) < 30:
            return {"error": "insufficient_data"}
        sma20 = sum(closes[-20:]) / 20
        sma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
        sma200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else None
        gains, losses = [], []
        for i in range(1, 15):
            delta = closes[-i] - closes[-i - 1]
            gains.append(max(delta, 0))
            losses.append(max(-delta, 0))
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        rs = avg_gain / avg_loss if avg_loss else 100.0
        rsi = 100 - (100 / (1 + rs))
        std = (sum((x - sma20) ** 2 for x in closes[-20:]) / 20) ** 0.5
        upper = sma20 + 2 * std
        lower = sma20 - 2 * std
        macd_line = (sum(closes[-12:]) / 12) - (sum(closes[-26:]) / 26)
        signal_line = sum([macd_line] + [((sum(closes[-12 + i:]) / 12) - (sum(closes[-26 + i:]) / 26)) for i in range(1, 10)]) / 9
        trend = "bullish" if sma20 > sma50 else "bearish" if sma20 < sma50 else "sideways"
        signals = []
        if rsi < 30:
            signals.append("oversold")
        elif rsi > 70:
            signals.append("overbought")
        if closes[-1] > upper:
            signals.append("breakout_upper_bollinger")
        elif closes[-1] < lower:
            signals.append("breakdown_lower_bollinger")
        if macd_line > signal_line:
            signals.append("macd_bullish_cross")
        elif macd_line < signal_line:
            signals.append("macd_bearish_cross")
        return {
            "symbol": symbol,
            "sma20": round(sma20, 4),
            "sma50": round(sma50, 4) if sma50 else None,
            "sma200": round(sma200, 4) if sma200 else None,
            "rsi14": round(rsi, 2),
            "bollinger": {"upper": round(upper, 4), "middle": round(sma20, 4), "lower": round(lower, 4)},
            "macd": {"macd": round(macd_line, 6), "signal": round(signal_line, 6), "histogram": round(macd_line - signal_line, 6)},
            "trend": trend,
            "signals": signals,
            "last_price": round(closes[-1], 4),
        }


class PortfolioEngine:
    """Portfolio tracking and risk management."""

    def __init__(self, market_data: MarketDataEngine):
        self.market_data = market_data
        self.cash: float = 500000.0
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        self.trades: List[Trade] = []
        self.realized_pnl: float = 0.0
        self.snapshots: List[PortfolioSnapshot] = []

    def get_positions(self) -> List[Dict]:
        results = []
        for symbol, position in self.positions.items():
            quote = self.market_data.get_quote(symbol)
            ltp = quote["price"] if quote else position.current_price
            position.current_price = ltp
            pnl = (ltp - position.average_price) * position.quantity * (1 if position.side == "long" else -1)
            results.append({
                "symbol": symbol,
                "quantity": position.quantity,
                "average_price": round(position.average_price, 4),
                "ltp": round(ltp, 4),
                "pnl": round(pnl, 2),
                "side": position.side,
                "product": position.product,
            })
        return results

    def portfolio_summary(self) -> Dict:
        holdings_value = 0.0
        unrealized_pnl = 0.0
        for symbol, position in self.positions.items():
            quote = self.market_data.get_quote(symbol)
            ltp = quote["price"] if quote else position.current_price
            position.current_price = ltp
            value = ltp * position.quantity
            holdings_value += value
            pnl = (ltp - position.average_price) * position.quantity * (1 if position.side == "long" else -1)
            unrealized_pnl += pnl
        total = self.cash + holdings_value
        self.snapshots.append(PortfolioSnapshot(
            timestamp=datetime.now(),
            cash=self.cash,
            holdings_value=holdings_value,
            total_value=total,
            realized_pnl=self.realized_pnl,
            unrealized_pnl=unrealized_pnl,
        ))
        return {
            "cash": round(self.cash, 2),
            "holdings_value": round(holdings_value, 2),
            "total_value": round(total, 2),
            "realized_pnl": round(self.realized_pnl, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "net_worth": round(total, 2),
            "positions": self.get_positions(),
        }

    def place_order(self, symbol: str, side: str, quantity: float, order_type: str = "market", price: Optional[float] = None, trigger_price: Optional[float] = None) -> Dict:
        side_enum = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
        type_enum = OrderType.MARKET if order_type.lower() == "market" else OrderType.LIMIT if order_type.lower() == "limit" else OrderType.SL if order_type.lower() == "sl" else OrderType.SL_LIMIT
        order_id = _generate_id("order")
        order = Order(
            order_id=order_id,
            symbol=symbol,
            side=side_enum,
            order_type=type_enum,
            quantity=float(quantity),
            price=price,
            trigger_price=trigger_price,
            status=OrderStatus.OPEN,
        )
        self.orders[order_id] = order
        filled = self._try_fill(order)
        return {
            "order_id": order_id,
            "status": filled.status.value,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "order_type": order_type,
            "filled_price": filled.price,
            "message": "order_placed_and_filled" if filled.status == OrderStatus.FILLED else "order_placed",
        }

    def cancel_order(self, order_id: str) -> Dict:
        order = self.orders.get(order_id)
        if not order:
            return {"error": "order_not_found"}
        if order.status != OrderStatus.OPEN:
            return {"error": f"order_not_open_{order.status.value}"}
        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now()
        return {"order_id": order_id, "status": "cancelled"}

    def _try_fill(self, order: Order) -> Order:
        quote = self.market_data.get_quote(order.symbol)
        if not quote:
            order.status = OrderStatus.REJECTED
            order.updated_at = datetime.now()
            return order
        ltp = quote["price"]
        if order.order_type == OrderType.MARKET:
            return self._execute(order, ltp)
        if order.price is not None and order.side == OrderSide.BUY and ltp <= order.price:
            return self._execute(order, order.price)
        if order.price is not None and order.side == OrderSide.SELL and ltp >= order.price:
            return self._execute(order, order.price)
        return order

    def _execute(self, order: Order, fill_price: float) -> Order:
        trade_id = _generate_id("trade")
        trade = Trade(
            trade_id=trade_id,
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=fill_price,
            timestamp=datetime.now(),
        )
        self.trades.append(trade)
        position = self.positions.get(order.symbol)
        if position is None:
            self.positions[order.symbol] = Position(
                symbol=order.symbol,
                quantity=order.quantity if order.side == OrderSide.BUY else -order.quantity,
                average_price=fill_price,
                current_price=fill_price,
                side="long" if order.side == OrderSide.BUY else "short",
            )
        else:
            if order.side == OrderSide.BUY:
                new_qty = position.quantity + order.quantity
                position.average_price = (position.quantity * position.average_price + order.quantity * fill_price) / new_qty if new_qty else fill_price
                position.quantity = new_qty
                position.side = "long"
            else:
                new_qty = position.quantity - order.quantity
                realized = (fill_price - position.average_price) * order.quantity if position.side == "long" else (position.average_price - fill_price) * order.quantity
                self.realized_pnl += realized
                position.quantity = new_qty
                if new_qty <= 0:
                    position.side = "short" if new_qty < 0 else "flat"
        order.status = OrderStatus.FILLED
        order.updated_at = datetime.now()
        return order

    def pnl_analytics(self) -> Dict:
        summary = self.portfolio_summary()
        returns = []
        values = [s.total_value for s in self.snapshots]
        if len(values) >= 2:
            for i in range(1, len(values)):
                returns.append((values[i] - values[i - 1]) / values[i - 1])
        win_rate = 0.0
        if self.trades:
            wins = [t for t in self.trades if (t.side == OrderSide.BUY and t.price < self.positions.get(t.symbol, Position(t.symbol, 0, t.price, t.price, "long")).average_price) is False and t.side == OrderSide.SELL]
            win_rate = 0.0
        return {
            "net_worth": summary["net_worth"],
            "realized_pnl": summary["realized_pnl"],
            "unrealized_pnl": summary["unrealized_pnl"],
            "open_positions": len([p for p in summary["positions"] if p["quantity"] != 0]),
            "completed_trades": len(self.trades),
        }


class TradingSkillsBackend:
    """Backend for trading and broker skills."""

    def __init__(self):
        self.market = MarketDataEngine()
        self.portfolio = PortfolioEngine(self.market)

    def skills(self) -> List[str]:
        return [
            "market_data",
            "stock_quotes",
            "crypto_trading",
            "forex_trading",
            "technical_analysis",
            "portfolio_tracking",
            "risk_management",
            "trade_execution",
            "broker_integration",
            "options_analytics",
            "futures_analytics",
            "backtesting",
            "paper_trading",
            "alert_management",
            "economic_calendar",
            "news_sentiment",
            "mutual_funds",
            "bond_analytics",
            "tax_reporting",
            "commodities_trading",
            "trading_journal",
            "algo_trading",
        ]

    def market_data(self, symbols: List[str]) -> Dict:
        quotes = self.market.get_quotes(symbols)
        return {"quotes": quotes}

    def stock_quotes(self, symbols: List[str]) -> Dict:
        return {"quotes": self.market.get_quotes(symbols)}

    def crypto_trading(self, symbols: List[str]) -> Dict:
        crypto = [s for s in symbols if s.endswith("USD")]
        return {"crypto": self.market.get_quotes(crypto)}

    def forex_trading(self, symbols: List[str]) -> Dict:
        forex = [s for s in symbols if "USD" in s and len(s) == 6]
        return {"forex": self.market.get_quotes(forex)}

    def technical_analysis(self, symbol: str) -> Dict:
        return self.market.technical_analysis(symbol)

    def portfolio_tracking(self) -> Dict:
        return self.portfolio.portfolio_summary()

    def risk_management(self, symbol: str, quantity: float) -> Dict:
        quote = self.market.get_quote(symbol)
        if not quote:
            return {"error": "symbol_not_found"}
        price = quote["price"]
        exposure = price * quantity
        stop_loss = round(price * 0.97, 4)
        take_profit = round(price * 1.06, 4)
        max_loss = exposure * 0.03
        position_risk = max_loss / self.portfolio.cash if self.portfolio.cash > 0 else 0
        return {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "exposure": round(exposure, 2),
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "max_loss": round(max_loss, 2),
            "position_risk_pct": round(position_risk * 100, 3),
            "suggested_size": round(self.portfolio.cash * 0.02 / max(1.0, abs(price - stop_loss)), 4),
        }

    def trade_execution(self, symbol: str, side: str, quantity: float, order_type: str = "market", price: Optional[float] = None, trigger_price: Optional[float] = None) -> Dict:
        return self.portfolio.place_order(symbol, side, quantity, order_type, price, trigger_price)

    def broker_integration(self, broker: str, action: str, payload: Dict) -> Dict:
        if action == "connect":
            return {"status": "simulated_connected", "broker": broker, "message": "Broker connection simulated"}
        if action == "disconnect":
            return {"status": "disconnected", "broker": broker}
        return {"status": "unknown_action", "broker": broker}

    def options_analytics(self, symbol: str) -> Dict:
        quote = self.market.get_quote(symbol)
        if not quote:
            return {"error": "symbol_not_found"}
        base = quote["price"]
        return {
            "symbol": symbol,
            "underlying_price": base,
            "expiries": ["this_week", "next_week", "monthly"],
            "atm_strike": round(base, 0),
            "sample_chain": [
                {"strike": round(base - 10, 0), "iv": 18.5, "oi": 12500, "volume": 980},
                {"strike": round(base, 0), "iv": 16.2, "oi": 24000, "volume": 1500},
                {"strike": round(base + 10, 0), "iv": 17.1, "oi": 13200, "volume": 870},
            ],
            "strategies": ["covered_call", "protective_put", "straddle", "strangle"],
        }

    def futures_analytics(self, symbol: str) -> Dict:
        return {
            "symbol": symbol,
            "status": "simulated_futures_mode",
            "recommended_contract": f"{symbol}_FUT",
            "open_interest": 45000,
            "roll_cost_bps": 3.2,
        }

    def backtesting(self, symbol: str, strategy: str) -> Dict:
        return {
            "symbol": symbol,
            "strategy": strategy,
            "cagr": round(((hash(strategy + symbol) % 100) / 10.0), 2),
            "max_drawdown": round(((hash(symbol + "dd") % 60) / 10.0), 2),
            "sharpe": round(((hash(strategy) % 100) / 20.0), 2),
            "win_rate": round(((hash(symbol) % 70) + 20, 2)[0], 2),
            "note": "simulated_backtest",
        }

    def paper_trading(self, action: str, payload: Dict) -> Dict:
        if action == "balance":
            return {"paper_balance": self.portfolio.cash, "currency": "INR"}
        if action == "reset":
            self.portfolio = PortfolioEngine(self.market)
            return {"status": "paper_portfolio_reset"}
        return {"status": "paper_trading_active"}

    def alert_management(self, action: str, payload: Dict) -> Dict:
        if action == "create":
            return {"alert_id": _generate_id("alert"), "status": "created", "payload": payload}
        if action == "list":
            return {"alerts": []}
        return {"status": "ok"}

    def economic_calendar(self) -> Dict:
        return {
            "events": [
                {"event": "RBI Policy Meet", "date": "2026-08-20", "impact": "high"},
                {"event": "US CPI Data", "date": "2026-08-22", "impact": "high"},
                {"event": "Fed Minutes", "date": "2026-08-24", "impact": "medium"},
                {"event": "Quarterly Earnings", "date": "2026-08-25", "impact": "medium"},
            ]
        }

    def news_sentiment(self, symbols: List[str]) -> Dict:
        return {
            "symbols": symbols,
            "sentiment": [{"symbol": s, "score": round(((hash(s) % 100) / 100.0), 2), "headline": f"Simulated news for {s}"} for s in symbols]
        }

    def mutual_funds(self, schemes: List[str]) -> Dict:
        return {
            "schemes": [
                {"code": s, "nav": round(((hash(s) % 1000) / 10.0), 2), "1y": round(((hash(s + "1y") % 200) / 10.0), 2)}
                for s in schemes
            ]
        }

    def bond_analytics(self, issuer: str) -> Dict:
        return {
            "issuer": issuer,
            "yield_to_maturity": round(((hash(issuer) % 80) / 10.0), 2),
            "duration": round(((hash(issuer + "d") % 30) / 10.0), 1),
            "credit_rating": "AAA",
        }

    def tax_reporting(self, year: str) -> Dict:
        return {
            "financial_year": year,
            "total_pnl": round(self.portfolio.realized_pnl, 2),
            "trades": len(self.portfolio.trades),
            "status": "simulated_tax_report",
        }

    def commodities_trading(self, symbols: List[str]) -> Dict:
        return {"commodities": self.market.get_quotes(symbols)}

    def trading_journal(self, action: str, payload: Dict) -> Dict:
        if action == "add":
            entry = {"timestamp": datetime.now().isoformat(), **payload}
            return {"status": "logged", "entry": entry}
        return {"status": "journal_updated", "action": action}

    def algo_trading(self, action: str, payload: Dict) -> Dict:
        if action == "status":
            return {"status": "algo_module_simulated", "running": False}
        return {"status": "algo_executed", "action": action}


backend = TradingSkillsBackend()


def handle_request(skill: str, payload: Dict) -> Dict:
    skill = (skill or "").lower().replace("-", "_")
    try:
        if skill in {"market_data", "stock_quotes", "crypto_trading", "forex_trading", "commodities_trading"}:
            return getattr(backend, skill)(payload.get("symbols", []))
        if skill == "technical_analysis":
            return backend.technical_analysis(payload.get("symbol", "RELIANCE"))
        if skill == "portfolio_tracking":
            return backend.portfolio_tracking()
        if skill == "risk_management":
            return backend.risk_management(payload.get("symbol", "RELIANCE"), float(payload.get("quantity", 1)))
        if skill == "trade_execution":
            return backend.trade_execution(payload.get("symbol", "RELIANCE"), payload.get("side", "buy"), float(payload.get("quantity", 1)), payload.get("order_type", "market"), payload.get("price"), payload.get("trigger_price"))
        if skill == "broker_integration":
            return backend.broker_integration(payload.get("broker", "zerodha"), payload.get("action", "connect"), payload)
        if skill == "options_analytics":
            return backend.options_analytics(payload.get("symbol", "RELIANCE"))
        if skill == "futures_analytics":
            return backend.futures_analytics(payload.get("symbol", "RELIANCE"))
        if skill == "backtesting":
            return backend.backtesting(payload.get("symbol", "RELIANCE"), payload.get("strategy", "moving_average_crossover"))
        if skill == "paper_trading":
            return backend.paper_trading(payload.get("action", "balance"), payload)
        if skill == "alert_management":
            return backend.alert_management(payload.get("action", "list"), payload)
        if skill == "economic_calendar":
            return backend.economic_calendar()
        if skill == "news_sentiment":
            return backend.news_sentiment(payload.get("symbols", ["RELIANCE", "BTCUSD"]))
        if skill == "mutual_funds":
            return backend.mutual_funds(payload.get("schemes", ["largecap", "midcap", "smallcap"]))
        if skill == "bond_analytics":
            return backend.bond_analytics(payload.get("issuer", "Government of India"))
        if skill == "tax_reporting":
            return backend.tax_reporting(payload.get("year", "2025-26"))
        if skill == "trading_journal":
            return backend.trading_journal(payload.get("action", "add"), payload)
        if skill == "algo_trading":
            return backend.algo_trading(payload.get("action", "status"), payload)
        return {"error": "unknown_trading_skill", "skill": skill}
    except Exception as e:
        return {"error": "trading_skill_failed", "skill": skill, "detail": str(e)}


if __name__ == "__main__":
    print(json.dumps(handle_request("portfolio_tracking", {}), indent=2))
    print("---")
    print(json.dumps(handle_request("technical_analysis", {"symbol": "RELIANCE"}), indent=2))
