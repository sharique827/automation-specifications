# ONDC:RET15 1.2.0 — Overview

## Summary

ONDC:RET15 is the domain standard for home appliance retail transactions on the ONDC network. It enables consumers to discover, purchase, and manage orders of household appliances (refrigerators, air conditioners, washing machines, etc.) across a network of independent electronics retailers and their delivery partners. The domain covers the full transaction lifecycle—from product discovery through delivery, returns, cancellations, and fulfillment exceptions.

## Sector & Purpose

**Sector:** Home appliances retail (consumer durables)

**Problem solved:** Home appliance shopping in India is fragmented across unconnected retailers, making it difficult for consumers to compare products and prices across stores and for smaller electronics retailers to reach customers beyond their local geography. ONDC:RET15 connects the fragmented home appliance retail ecosystem by allowing independent electronics stores to list their appliance inventory on ONDC-enabled buyer platforms (BAPs), giving consumers unified access to products from multiple retailers while enabling retailers to compete on equal footing with large platforms.

## Real-World Actors

- **Consumers:** Individuals shopping for household appliances (air conditioners, refrigerators, ovens, washing machines, water heaters, etc.)
- **Electronics stores:** Independent retailers, single-brand outlets, and appliance dealerships that stock and sell home appliances
- **Logistics providers:** Delivery and fulfillment networks that handle order fulfillment and reverse logistics (for returns and cancellations)
- **Buyer platforms (BAPs):** Consumer-facing apps and websites aggregating appliance listings from multiple electronics stores
- **Seller platforms (BPPs):** Retailer-facing backends that list appliance inventories and manage orders

## Use Cases

- **Purchase appliances:** Consumers browse catalogs from multiple electronics stores and purchase home appliances through unified BAP interfaces
- **Manage orders:** Track delivery status, confirm receipt, and manage order timelines across retailers
- **Return appliances:** Initiate returns for full or partial orders with transparent return policies and reverse logistics
- **Cancel orders:** Buyer-initiated cancellations before fulfillment and merchant-initiated cancellations (e.g., RTO—return-to-origin for undeliverable orders)
- **Discover inventory:** Full catalog discovery at onboarding and incremental catalog refreshes as retailers update stock
- **Handle exceptions:** Manage out-of-stock scenarios and delivery failures gracefully

## Key Concepts

- **Full catalog vs. incremental discovery:** Electronics stores can push their complete appliance inventory on initial onboarding or continuously push incremental updates (new stock, price changes) to avoid duplicate data
- **Prepaid delivery flows:** Orders confirmed and fulfilled with prepayment (cash-on-delivery flows are out of scope for this version)
- **Return-to-origin (RTO):** When a delivery cannot be completed, the appliance is returned to the merchant's fulfillment point
- **Partial order returns:** Consumers may return specific items in multi-item orders (e.g., returning a fridge but keeping the oven from the same order)
- **Inventory synchronization:** Real-time or near-real-time catalog updates ensure BAPs display accurate stock and pricing

## Example Scenario

A consumer uses an ONDC-enabled buyer app to search for an air conditioner. The app shows listings from three local electronics stores participating in ONDC. The consumer selects an air conditioner from one store, completes prepayment, and the order is confirmed. The electronics store (BPP) processes the order through their logistics partner, who delivers the air conditioner to the consumer's home. The consumer confirms receipt in the buyer app. Two weeks later, the air conditioner develops a fault. The consumer initiates a return through the app, the logistics partner picks it up, and it is returned to the electronics store's warehouse for inspection. If approved, the store processes a refund and the return is marked complete in the ONDC system. Throughout the lifecycle—discovery, purchase, delivery confirmation, return initiation, and refund—the ONDC:RET15 domain provides the standardized message flows that let the consumer's app, the electronics store's backend, and the logistics provider communicate.
