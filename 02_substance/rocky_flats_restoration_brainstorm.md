# Rocky Flats: Full Restoration Brainstorm

*Seed document. Created 2026-06-23. This is a brainstorm, not a plan. It collects ideas and labels each by how mature it is, so we do not confuse a hope with a capability. Every figure is attributed or labeled a goal. Nothing here is a commitment.*

---

## The north star (goal)

Take the Rocky Flats site, all of it, and return it to a fully clean, certified, liveable place. Not "managed in place". Not "safe enough behind a fence". Clean to the point that an independent body certifies it, the community accepts it, and people would choose to live, work, and raise children there. Reverse the damage of the past, in the open, with honesty as the method.

This is a multi-decade moonshot. We should say that plainly and still pursue it.

---

## The honest starting point

What is there now. The Rocky Flats National Wildlife Refuge is about 5,237 acres of buffer land around a former nuclear weapons plant that machined plutonium pits (source: U.S. Fish and Wildlife Service; Wikipedia). The most contaminated core, the Central Operable Unit, was not restored to a blank slate. The Department of Energy retains it under permanent use restrictions, groundwater treatment, and long-term monitoring (source: GAO-06-352).

What was already done. A cleanup ran roughly ten years and cost about $7 billion, completed in 2005, removing the plutonium buildings and roughly 500,000 cubic meters of radioactive waste (source: GAO; Yale E360). Full removal of all contaminated soil and infrastructure was priced at about $37 billion over about 65 years, and that option was deliberately not taken (source: GAO; Yale E360). So "cleaned up" meant "stabilized and managed," not "made pristine."

The core constraint. The contaminant of concern is plutonium-239, with a half-life near 24,100 years, per standard nuclear reference data. We cannot wait it out. We cannot destroy it chemically. Any chemical or physical method moves the plutonium; it does not eliminate it. Eliminating a plutonium atom requires a nuclear process (fission or transmutation).

The one-line restatement. To truly clear the site we must do one of two things with the plutonium: move all of it somewhere permanent, or destroy it in a reactor or accelerator. Decay is not on the table on any human timescale.

---

## Approach families

Each idea below carries a maturity tag:
- **Today**: proven and deployable now.
- **Emerging**: demonstrated at pilot or lab scale, not yet operational at site scale.
- **Frontier**: physics is sound, no operational plant exists, multi-decade.
- **Speculative**: an idea worth exploring, not yet shown to work for this problem.

### A. Map it to the gram (shrink the problem first)

Rocky Flats contamination is patchy, not uniform. The single highest-leverage move is to characterize it at very high resolution, so we only treat the soil that is actually contaminated instead of all of it. This is where Photon Mountain's core competence, light, contributes directly.

- **Laser-induced breakdown spectroscopy (LIBS), drone and rover mounted.** Fire a pulsed laser at the soil, read the plasma, get near real-time elemental readings with little sample prep. LIBS has detected a plutonium surrogate (cerium oxide) in soil with machine learning at detection limits around 0.015 to 0.022 weight percent (sources: Optica, Applied Optics). LIBS payloads have flown on autonomous rovers (source: MDPI). Maturity: **Emerging** for plutonium specifically; the surrogate work is promising, field plutonium mapping is not yet operational.
- **Hyperspectral and photonic sensor networks.** Persistent, autonomous surveying to build a living contamination map and watch for wind-driven resuspension. Maturity: **Emerging**.
- **AI over the sensor stream.** Turn millions of readings into a centimeter-scale 3D contamination model that tells crews exactly where to dig. Maturity: **Today** for the analytics, gated by sensor maturity.

Why this matters: if precise mapping cuts the volume that needs treatment by a large factor, every downstream cost in this document drops with it.

### B. Separate and concentrate (reduce the mass that must be handled)

The goal here is to pull plutonium out of large volumes of soil and leave behind clean bulk soil plus a small, concentrated stream.

- **Soil washing and chemical leaching.** Wash or leach plutonium off soil particles, then handle the concentrated residue. Established for some radionuclides, but effectiveness depends heavily on soil type, and Rocky Flats soils are clay and silt rich, which is the hard case (source: ResearchGate review; Frontiers). Maturity: **Today elsewhere, site-uncertain here**.
- **Electrokinetic remediation.** Run a low electric field through the soil to drive plutonium toward a collection electrode. A field-scale trial treated about 4 tonnes of plutonium-contaminated soil over 60 days and showed plutonium mobilizing toward the anode (source: ScienceDirect). Uranium analogs reach roughly 61 to 99 percent removal, but slowly, and clay-rich soils are a known challenge (source: Frontiers). Maturity: **Emerging / pilot**.
- **Mechanical sorting and segmented-gate systems.** Use real-time radiation sensing on conveyed soil to divert only the hot fraction. Maturity: **Today**.

Output of this stage: most of the dirt comes back clean, and the plutonium ends up in a much smaller package.

### C. Capture chemically or biologically (polish and immobilize)

- **Selective chelators and nanomaterial sorbents.** Molecules and engineered surfaces that grab actinides selectively for extraction or capture. Maturity: **Emerging / lab**.
- **Phytoremediation and bioremediation.** Plants and microbes that take up or bind plutonium. Honest limit: plutonium has low bioavailability, so plant uptake is small, and microbial methods mostly immobilize, not remove (source: remediation reviews). Useful as a polishing or stabilizing step, not as the main engine. Maturity: **Limited / research**.

### D. Destroy it for good (the only path that is actually "clean")

Everything above relocates plutonium. To eliminate it, the concentrated stream from stage B and C goes to a nuclear process that fissions the plutonium into shorter-lived or stable products.

- **Fast reactors and accelerator-driven subcritical systems (ADS).** Plutonium-239 fissions. Accelerator-driven systems can burn actinides while staying subcritical, since fission stops when the accelerator turns off (sources: Annual Reviews; World Nuclear Association). Honest limits: these consume concentrated, fabricated feed, not dilute soil, so they sit at the end of the chain. No commercial ADS plant operates today. This is a multi-decade, heavy-infrastructure effort with its own licensing and waste questions. Maturity: **Frontier**.
- This is the difference between "we moved Colorado's plutonium to someone else's desert" and "we ended it." The honest, complete version of the goal points here.

### E. Water, residue, and the long tail

- **Groundwater.** The site already runs shallow groundwater treatment and has a solar ponds plume under management (source: ITRC; GAO). Full restoration has to close these out, not just maintain them.
- **Final disposition of the concentrate.** If we do not destroy it, it needs a permanent home, which reopens the national repository question. This is the argument for pushing toward stage D.

---

## The Photon Mountain angle (where we honestly fit)

We should be clear-eyed about which parts of this are ours to lead and which are national-scale efforts we would join.

- **Sensing and mapping is our wheelhouse.** Photonic sensors, LIBS, and AI-driven characterization are light technologies, they are near-term, and precise mapping is the highest-leverage early win. This is a credible Photon Mountain contribution, not a stretch.
- **The research anchors are here.** Boulder and Golden hold unusual density: NIST and JILA for precision measurement, plus CU Boulder and the Colorado School of Mines. NLR (formerly NREL) anchors the energy research. A site-characterization and remediation-science effort has a natural home in this corridor.
- **Light as energy to power the work.** Remediation at scale is energy hungry. The corridor's solar and energy research is a thematic fit for powering it cleanly, which keeps the restoration consistent with its own values.
- **The brand thesis.** "Reverse the damage of the past and build the future with light" is a real, honest story. It holds if we lead with the parts we can actually do and label the rest as the long horizon.

What we should not claim: that photonics alone cleans the site, that any of this is ready today, or that we have a cost or timeline. We have a research agenda and a direction.

---

## The non-technical half (just as hard as the science)

- **Ownership.** DOE retains the Central Operable Unit. Nothing happens there without the federal government as a partner.
- **Regulation.** The site sits inside the CERCLA / Superfund framework, with EPA and the Colorado Department of Public Health and Environment (CDPHE) as regulators. "Clean" is a legal and scientific standard, not a feeling.
- **Community trust and consent.** The community is genuinely divided about Rocky Flats, including about the refuge opening to public trails in 2018. Trust is the scarce resource. Radical transparency, open data, and independent verification are not optional extras here; they are the product.
- **Funding and liability.** Numbers like $37 billion (the historical full-removal estimate) signal the order of magnitude. Who pays, who carries liability, and who certifies the end state are first-order questions.
- **Defining "done."** We need an explicit, certifiable definition of "completely clear" and "liveable," agreed with regulators and the community, before we promise it. Otherwise the goal cannot be checked.

---

## Hard truths (so we do not oversell)

1. No method on the shelf today fully clears dispersed plutonium from soil. We would be advancing the field, not applying a catalog.
2. Every non-nuclear step relocates plutonium. Only stage D ends it.
3. Soil type at Rocky Flats (clay and silt) is the difficult case for the most promising separation methods.
4. The full path is plausibly multi-decade and national in scale. Photon Mountain can lead the front end and convene the rest.
5. The fastest credible win is characterization, not removal. Map first.

---

## A staged path (direction, not schedule)

1. **Characterize.** Build the highest-resolution contamination map ever made of the site, using photonic sensing and AI. Shrink the problem.
2. **Pilot.** Run small, transparent, well-instrumented field trials of separation methods (soil washing, electrokinetics) on mapped hotspots, with published results.
3. **Scale separation.** Move clean bulk soil back; concentrate the plutonium into a small, well-characterized stream.
4. **Destroy.** Route the concentrate into the national actinide-destruction path (fast reactor or ADS) as that capability matures.
5. **Certify and return.** Independent verification against an agreed clean standard, then phased return of the land.

---

## First concrete next steps (cheap, honest, now)

- Stand up a one-page "what would have to be true" list for full restoration, and pressure-test it with a health physicist and a remediation engineer.
- Map the stakeholders and existing data: DOE, EPA, CDPHE, FWS, CU, Mines, NIST, and the local advocacy groups, plus the public administrative record.
- Scope a characterization-only pilot proposal (LIBS plus drones plus AI mapping) as Photon Mountain's credible entry point.
- Draft the transparency and consent principles first, before any technical pitch.
- Keep this document honest: update maturity tags as the science moves, and never let an aspiration drift into a claim.

---

## Sources

- [Rocky Flats National Wildlife Refuge (U.S. Fish and Wildlife Service)](https://www.fws.gov/refuge/rocky-flats)
- [Rocky Flats Plant (Wikipedia)](https://en.wikipedia.org/wiki/Rocky_Flats_Plant)
- [GAO-06-352, Nuclear Cleanup of Rocky Flats](https://www.gao.gov/assets/gao-06-352.pdf)
- [Rocky Flats: A Wildlife Refuge Confronts Its Radioactive Past (Yale E360)](https://e360.yale.edu/features/rocky_flats_wildlife_refuge_confronts_radioactive_past)
- [Electrokinetic remediation of plutonium-contaminated soil, pilot trial (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0304389410015967)
- [Electrokinetic remediation of uranium-contaminated soil, review (Frontiers, 2025)](https://www.frontiersin.org/journals/chemical-engineering/articles/10.3389/fceng.2025.1687808/full)
- [Stacked-ensemble ML for surrogate plutonium detection in soil via LIBS (Applied Optics)](https://opg.optica.org/ao/abstract.cfm?uri=ao-64-16-D122)
- [Accelerator-driven systems for nuclear waste transmutation (Annual Reviews)](https://www.annualreviews.org/doi/full/10.1146/annurev.nucl.48.1.505)
- [Accelerator-driven nuclear energy (World Nuclear Association)](https://world-nuclear.org/information-library/current-and-future-generation/accelerator-driven-nuclear-energy)
- [Rocky Flats Solar Ponds Plume remediation (ITRC)](https://rmcs-1.itrcweb.org/6-3-rocky-flats-solar-ponds-plume-colorado/)
