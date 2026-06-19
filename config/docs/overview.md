# ONDC:RET16 1.2.0 — Overview

## Summary

ONDC:RET16 enables merchants and consumers to transact **home and kitchen products over ONDC**—a standardized network protocol that lets independent sellers list goods, buyers discover them, and both parties execute complete order lifecycles. This domain covers everything from product discovery through delivery, returns, and cancellations, removing friction between home goods retailers and a growing digital customer base.

## Sector & Purpose

**Sector:** Home & Kitchen Retail

The home and kitchen goods category includes everyday items—cookware, small appliances, storage, utensils, bedding, and household essentials—traditionally sold through dedicated retail chains, online marketplaces, or neighborhood shops. 

**Problem Solved:** Today, merchants (from large chains to small independent retailers) operate in isolated storefronts or rely on a handful of centralized e-commerce platforms. Consumers must search multiple apps to compare prices and availability. **ONDC:RET16 creates a shared digital infrastructure** where any merchant can list home & kitchen inventory and any buyer can access it through any ONDC-enabled shopping app—similar to how airlines operate on shared booking networks. This reduces platform lock-in, lowers seller costs, and gives consumers genuine choice.

## Real-World Actors

- **Sellers:** Home goods retailers—from large chains (appliances, furniture) to neighborhood stores (kitchenware, linens) to small manufacturers—who want to reach customers beyond their own website
- **Buyers:** Consumers shopping for household items (pots, pans, storage boxes, cleaning tools, bedding) who use ONDC-enabled apps to browse, compare, and purchase
- **Delivery Partners:** Logistics networks that fulfill orders from sellers to buyers
- **ONDC Network:** The protocol infrastructure connecting all parties

## Use Cases

- Consumers discovering home and kitchen products through full or incremental catalog search
- Buyers placing and confirming orders for prepaid purchases
- Buyers receiving items and managing returns (full or partial orders)
- Buyers canceling orders before fulfillment
- Sellers managing out-of-stock scenarios
- Sellers initiating returns-to-origin (RTO) and partial order cancellations after fulfillment issues

## Key Concepts

- **Catalog Discovery:** Sellers expose full or incrementally-updated product catalogs; buyers search and browse in real time
- **Complete Order Lifecycle:** From placement, confirmation, and shipment through delivery, return, and resolution
- **Cancellations & Returns:** Both buyers and sellers can cancel or return orders; the protocol handles both directions
- **Inventory Synchronization:** Out-of-stock signals and incremental catalog refreshes keep availability accurate across the network
- **Prepaid Fulfillment:** Orders are paid before shipment, reducing settlement complexity

## Example Scenario

A consumer in Bangalore opens an ONDC-enabled shopping app and searches for "stainless steel mixing bowls." The app queries multiple home goods sellers on the ONDC network—a large kitchenware chain, a local kitchen store, and a small manufacturer—each with current inventory and pricing. The consumer picks a set from the local store, pays upfront, and receives a confirmation.

Three days later, the bowls arrive. If one is dented, the consumer initiates a return through the app. The return flows back through ONDC; the seller logs the damage and issues a refund or replacement. Meanwhile, if the seller had run low on stock, they pushed an incremental catalog update earlier that day, removing the bowls from other buyers' search results—all without manual intervention, all coordinated through ONDC:RET16.
