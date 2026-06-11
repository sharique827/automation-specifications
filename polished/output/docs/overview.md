# ONDC:RET14 1.2.0 — Overview

## Summary

ONDC:RET14 is the ONDC network domain for retail electronics goods. It enables consumers to discover, purchase, and manage orders for electronics products from online stores operating on the ONDC network. Version 1.2.0 defines the full transactional lifecycle — from catalog search through order confirmation, fulfillment tracking, cancellations, and returns.

## Sector & Purpose

**Sector:** Retail — Consumer Electronics

Electronics retail involves high-value, specification-sensitive goods (televisions, smartphones, laptops, appliances, and accessories) that require rich catalog data, reliable fulfillment tracking, and well-defined post-purchase workflows. Selling electronics goods online presents distinct operational challenges: catalogs change rapidly with new variants and availability, prepaid orders require careful fulfillment confirmation, and returns or cancellations involve logistics coordination that differs from simpler product categories.

ONDC:RET14 solves this by providing a standardized protocol layer so any electronics seller can list inventory and transact with any buyer-side app on the network — without bilateral integrations — while covering the full order lifecycle including out-of-stock handling, return-to-origin (RTO) flows, and partial order cancellations.

## Real-World Actors

| Actor | Who They Are in Practice |
|---|---|
| **Consumer / Buyer** | An individual shopping for electronics — browsing for a television, smartphone, laptop, or home appliance — using a buyer-facing app or platform connected to the ONDC network. |
| **Electronics Store / Seller** | A retailer or brand selling electronics goods online: a national electronics chain, a regional dealer, a brand's direct-to-consumer store, or a marketplace seller with an electronics catalog. |
| **Logistics / Fulfillment Provider** | The delivery partner who picks up the item from the seller and delivers it to the consumer, and who may also handle return pickups and RTO shipments. |

## Use Cases

- **Product Discovery** — A consumer searches for electronics products and receives a seller's full catalog or incrementally refreshed listings, including custom menus, pricing, and item availability, across the city or region.
- **Prepaid Order Fulfillment** — A consumer selects an electronics item, places a prepaid order, receives confirmation, and tracks the shipment through to delivery.
- **Buyer-Side Order Cancellation** — A consumer cancels an electronics order after confirmation, triggering acknowledgment and cancellation status updates from the seller.
- **Buyer-Initiated Return** — A consumer initiates a return for a full electronics order or specific items within a partial order, with the flow covering return authorization, pickup coordination, refund settlement, and closure.
- **Merchant-Side RTO and Partial Cancellation** — A seller manages a return-to-origin scenario (e.g., failed delivery) or cancels specific items or quantities from a partially fulfillable order, with status updates propagated back to the buyer.
- **Out-of-Stock Error Handling** — A seller accepts a buyer's item selection but responds with a structured out-of-stock error when the requested product or variant is unavailable, allowing the buyer app to surface this gracefully.
- **Incremental Catalog Refresh** — A buyer app repeatedly polls for updated seller catalog data, capturing newly listed products, revised pricing, and changed availability in near real time.

## Key Concepts

- **Catalog Discovery vs. Incremental Push/Pull** — Electronics catalogs can be large and frequently updated. RET14 supports both a full city-wide catalog delivery on search and incremental refresh patterns (push and pull), so buyer apps always reflect current stock and pricing without fetching the entire catalog each time.
- **Prepaid Order Lifecycle** — Electronics transactions in this domain follow a prepaid flow: payment is collected upfront, and the protocol tracks each stage from confirmation through fulfillment status updates to final delivery.
- **Return and RTO Workflows** — Electronics returns are operationally distinct: they may be full-order or partial-item returns, and failed deliveries may trigger an RTO (Return to Origin) back to the seller. Both paths have defined states for authorization, pickup, and closure.
- **Partial Order Operations** — A single electronics order may contain multiple items. The domain explicitly supports partial cancellations (cancelling some items, not all) and partial returns, with granular status tracking per item or quantity.
- **Out-of-Stock Error Protocol** — Rather than silently failing, the domain defines a structured error response on `on_select` when an item or variant is unavailable, giving integrators a clear signal to handle availability failures in the buyer experience.

## Example Scenario

A consumer opens an app connected to the ONDC network and searches for a television. The app sends a `search` request; nearby electronics stores respond via `on_search` with their catalogs — including available TV models, variants (screen size, resolution), and prices. The consumer selects a 55-inch smart TV from a local electronics store, and the store confirms availability and pricing via `on_select`.

The consumer proceeds to checkout with a prepaid payment. The store acknowledges the order via `on_confirm`, and the television is dispatched. The buyer app receives a series of `on_status` updates — order packed, picked up, out for delivery — until the TV is delivered and the order is marked complete.

If the consumer finds the television is damaged on arrival, they initiate a return through the app. The store authorizes the return, a logistics partner schedules a pickup, and after the item is collected and inspected, a refund is settled and the return is closed. If instead the delivery had failed entirely, the seller's system would process an RTO flow — marking the shipment as returning to origin and updating the order status accordingly.
