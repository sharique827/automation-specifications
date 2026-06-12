# ONDC:TRV10 2.1.0 — Overview

## Summary

ONDC:TRV10 is a domain specification for ride-hailing services that enables passengers to book cars, bikes, buses, and other vehicles through any ONDC-enabled platform on a shared network. Instead of being locked into a single app, consumers can search for and book rides across multiple ride-hailing providers, and service providers can offer their vehicles and drivers to multiple consumer platforms simultaneously.

## Sector & Purpose

This domain addresses the ride-hailing and transportation sector. The problem it solves is **consumer lock-in**: historically, passengers must download separate apps for each ride-hailing service in their city, and drivers must work through multiple platforms to maximize earnings. ONDC:TRV10 creates an interoperable network where a single consumer application can request rides from any participating provider on the network, and any driver or fleet can serve requests from any consumer platform.

## Real-World Actors

The transactions happen between **consumers** (passengers looking for a ride) and **ONDC-enabled ride-hailing platforms** (the companies that own the vehicles, manage drivers, and operate fleets). A passenger using one platform can now request service from any driver or fleet registered on that network, regardless of which company traditionally "owns" that driver. Drivers benefit by accessing rider demand from multiple sources without juggling separate apps.

## Use Cases

- **On-demand ride booking** — A passenger requests an immediate ride (car, bike, or bus); the system assigns an available driver and confirms the ride
- **Scheduled rides** — A passenger books a ride in advance for a specific date and time
- **Rental rides** — A passenger books a vehicle for an extended hourly or daily period
- **Ride with multiple stops** — A passenger requests a ride that includes multiple pickup or dropoff locations
- **Ride cancellation and updates** — Both passengers and drivers can cancel rides, or modify stops during an active ride
- **Pre-order bidding** — Drivers or platforms can bid on upcoming ride requests before they are confirmed
- **Post-ride tips** — Passengers can add tips after a ride is completed
- **Ride failure recovery** — The system handles cases where a driver is not found or becomes unavailable, with fallback and rerouting logic

## Key Concepts

- **Network interoperability** — Any ONDC-enabled ride-hailing platform can offer service to any consumer app on the network; no single company controls access
- **Booking and assignment** — A ride request is structured, offered to available drivers or platforms, and confirmed when a driver accepts
- **Ride lifecycle management** — From booking through cancellation, updates, and completion, the system tracks status and handles exceptions
- **Multiple vehicle types** — The domain supports cars, bikes, buses, and other vehicle classes in a single transaction model
- **Multi-stop and flexible routing** — Rides can include multiple pickup and dropoff points, with the ability to add or modify stops during transit

## Example Scenario

A consumer uses a ride-hailing app (Platform A) and requests a car from their home to the office. The app broadcasts this request to all available ONDC ride-hailing providers on the network. A driver working for Cab Company B (different from Platform A) accepts the ride through the ONDC network. The system assigns the driver, shares real-time location and estimated arrival with the consumer through Platform A's interface, and confirms the ride. Fifteen minutes later, the passenger requests to add a second stop at a coffee shop. The app updates the ride plan, and the driver adjusts the route. When the ride ends, the passenger tips the driver through the same app. Throughout, the consumer experienced a seamless transaction without downloading multiple apps, and the driver served multiple platforms from a single vehicle.
