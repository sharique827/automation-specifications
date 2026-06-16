# ONDC:TRV12 2.0.0 — Overview

## Summary

ONDC:TRV12 is the travel domain for booking intercity public transport—airlines and buses—on the ONDC network. It lets consumers search, book, and manage tickets across multiple transport operators in a single platform, while enabling airlines and bus companies to list and sell seats directly to end users.

## Sector & Purpose

This domain serves the **intercity public transport sector**, covering long-distance flights and bus services. The core problem it solves is fragmentation: today, consumers must visit separate websites or apps for each airline, each bus operator. ONDC:TRV12 unifies that experience, allowing any consumer-facing application (airline app, travel portal, marketplace) to tap into inventory from multiple operators through a single standardized network, while operators gain access to new distribution channels without building separate integrations.

## Real-World Actors

- **Consumers**: People booking trips between cities—whether flying across regions or taking long-distance buses. They want options, convenience, and clear pricing.
- **Airlines**: Operators with seat inventory to sell; they list flights and manage bookings, cancellations, and customer service through the ONDC network.
- **Bus Operators**: Intercity bus companies offering routes; they list schedules and seat availability just like airlines.
- **Platforms**: Travel booking apps, OTA sites, or marketplaces that aggregate these options for consumers and handle the transaction experience.

## Use Cases

- Searching for airline flights by route and date, browsing available airlines and prices
- Booking single or multiple airline tickets in one transaction (families, groups)
- Searching for intercity bus services and booking seats
- Cancelling bookings—initiated by either the consumer or the operator
- Partial cancellations when a customer wants to cancel only some tickets in a multi-ticket order
- Rating and reviewing flights or bus rides after travel
- Code-based search flows (searching by station codes for buses, airline codes for flights)
- Resolving disputes or service issues through the ONDC complaint mechanism (IGM)

## Key Concepts

- **Airline and Bus Booking as Parallel Flows**: The domain handles two distinct transport modes with different attributes (flights have aircraft classes and routing; buses have station stops and route types), but both follow similar booking and cancellation workflows.
- **Code-Based Discovery**: Operators use standardized codes (airline IATA codes, bus station codes) to tag inventory; consumers and platforms use these to search efficiently.
- **Ticket Inventory Management**: Whether booking one seat or ten, the system tracks availability, holds, and fulfillment per transaction—critical for managing overbooking and real-time availability.
- **Cancellation Workflows**: Both parties (buyer and seller) can initiate cancellations with different rules and refund implications; the domain specifies how these are processed.
- **Service Quality and Dispute Resolution**: Post-booking ratings and IGM (Integrated Grievance Mechanism) enable feedback loops and fair dispute handling across the network.

## Example Scenario

**A family booking a multi-city trip on the ONDC network:**

A consumer uses a travel platform integrated with ONDC:TRV12 to book flights from Mumbai to Delhi for four people. The platform queries multiple airlines' inventory, finds a suitable flight, and completes the booking in one transaction—all four tickets together. Two weeks later, one family member's plans change; the consumer cancels that one ticket through the ONDC platform, which sends the cancellation to the airline. The airline processes a partial refund per its policy.

After the trip, the family rates the airline's service (on-time, courteous crew, good food) through the ONDC platform. The rating feeds back into the network, helping other consumers see service quality signals.

Later, when planning an intercity bus trip for a similar multi-city journey, the same consumer uses the same ONDC platform to search buses between intermediate cities—the discovery and booking flow is comparable to the airline experience, but adapted for bus routes and station-based stops. The unified experience across transport modes is the real-world value ONDC:TRV12 delivers.
