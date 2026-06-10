# ONDC:RET12 1.2.0 — Overview

## Summary

ONDC:RET12 is the ONDC network domain for fashion retail, covering the discovery, ordering, fulfillment, and post-purchase management of clothing and apparel products. It enables retail clothing stores to list and sell their products online through the open ONDC network, reaching buyers without depending on closed, proprietary marketplaces. Version 1.2.0 defines 8 flows and 21 actions spanning the full commerce lifecycle — from catalog search through delivery, cancellation, and returns.

## Sector & Purpose

**Sector:** Fashion retail (apparel, clothing, and related accessories sold by physical or online retail stores)

The core problem this domain solves is access and dependency. Independent clothing retailers have historically had to rely on dominant e-commerce platforms — such as Amazon or Flipkart — to reach online shoppers, bearing the cost of high commission structures and platform lock-in. ONDC:RET12 gives these retail shops a standardised, interoperable way to list their fashion products on the open network, so that any ONDC-compatible buyer application can discover and purchase from them directly. The playing field is levelled: a small local boutique and a large apparel brand participate on the same open protocol.

## Real-World Actors

| Actor | Who They Are in Practice |
|---|---|
| **Consumer (Buyer)** | A shopper looking for clothing items — jeans, T-shirts, ethnic wear, accessories — browsing via any ONDC-enabled buyer app |
| **Clothing Store (Seller)** | A fashion retailer — whether a neighbourhood garment shop, a regional brand, or a dedicated online fashion label — that has listed its inventory on the ONDC network via a seller-side platform |
| **Buyer Platform** | The app or website the consumer uses to search and place orders (e.g. a shopping app integrated with ONDC) |
| **Seller Platform** | The technology provider that onboards the clothing store onto the ONDC network, manages its catalog, and processes orders on its behalf |
| **Logistics Provider** | The delivery partner who picks up the packed order from the store and fulfils delivery to the consumer's address |

## Use Cases

- **Fashion product discovery** — A shopper searches for clothing items (by category, style, size, or city) and receives catalog results from multiple stores across the network
- **Incremental catalog updates** — A clothing store pushes live updates to its product listings (price changes, new arrivals, style additions) without a full catalog refresh
- **Prepaid order placement and delivery** — A consumer selects items, pays online, and the order is confirmed and dispatched to their address
- **Buyer-initiated returns** — A shopper initiates a return for a full order or specific items (e.g. wrong size, damaged goods), triggering a reverse logistics flow
- **Buyer-side order cancellation** — A consumer cancels an order before or shortly after confirmation
- **Merchant-side RTO and partial cancellation** — The seller initiates a Return to Origin (RTO) when delivery fails, or cancels part of an order (e.g. one item is out of stock post-confirmation)
- **Out-of-stock error handling** — The network surfaces a standardised error when a requested item becomes unavailable during the order flow

## Key Concepts

- **Fashion catalog structure** — Product listings in this domain carry fashion-specific attributes such as size, colour, style, gender category, and material; integrators must map their inventory to these fields correctly for search and filtering to work
- **Full vs. incremental catalog push** — Stores can either publish their entire catalog at once (full catalog) or stream changes in real time (incremental push/pull); understanding when to use each mode is essential for keeping listings accurate without overloading the network
- **Fulfillment states in fashion** — Fashion orders have well-defined lifecycle states (confirmed → packed → shipped → delivered → return-initiated → returned) and integrators must handle state transitions for both forward delivery and reverse logistics
- **Return and RTO flows** — Fashion has a relatively high return rate; the domain explicitly models buyer-initiated returns (partial or full) and merchant-initiated RTO separately, each with its own action sequence
- **Out-of-stock signalling** — Because fashion inventory (especially sized items) can deplete quickly, the domain provides a dedicated error-code flow so buyer apps can handle unavailability gracefully rather than letting orders fail silently

## Example Scenario

A consumer opens an ONDC-enabled shopping app and searches for jeans and T-shirts in their city. The buyer app queries the ONDC network and returns results from several local clothing stores that have listed their inventory — stores that previously could only reach online shoppers by paying steep commissions to platforms like Amazon or Flipkart.

The shopper picks a pair of jeans from one store and two T-shirts from another, pays online (prepaid flow), and both orders are confirmed. Each store's seller platform receives the order, packs the items, and hands them to a logistics provider. The consumer receives both shipments at their door.

A few days later, the jeans don't fit. The consumer raises a return request through the buyer app. The return flow is triggered: a reverse pickup is scheduled, the item is collected from the consumer's address, and once the store confirms receipt, a refund is processed.

Meanwhile, the clothing store — a neighbourhood garment shop with no in-house tech team — has been operating entirely through its seller platform, gaining access to the same pool of online shoppers as any large retailer, without ceding margin to a monopolised marketplace.
