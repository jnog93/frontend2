import { mdiDotsVertical } from "@mdi/js"; //icons
import "@thomasloven/round-slider";
import {
  css,
  CSSResultGroup,
  html,
  LitElement,
  PropertyValues,
  TemplateResult,
} from "lit"; //lit
import { customElement, property, state } from "lit/decorators"; //lit
import { classMap } from "lit/directives/class-map"; //lit
import { styleMap } from "lit/directives/style-map"; //lit
import { applyThemesOnElement } from "../../../common/dom/apply_themes_on_element"; //apply theme
import { fireEvent } from "../../../common/dom/fire_event"; //fire events
import { computeStateDisplay } from "../../../common/entity/compute_state_display"; //display
import { computeStateName } from "../../../common/entity/compute_state_name"; //compute state of entity
import { stateIcon } from "../../../common/entity/state_icon"; //escrever o icon, cor do icon
import "../../../components/ha-card";
import "../../../components/ha-icon-button"; //definições
import { UNAVAILABLE, UNAVAILABLE_STATES } from "../../../data/entity"; //constantes
import { LightEntity, lightSupportsDimming } from "../../../data/light"; // busca estados à backend
import { ActionHandlerEvent } from "../../../data/lovelace"; //para fazer o toggle e acçoes
import { HomeAssistant } from "../../../types";
import { actionHandler } from "../common/directives/action-handler-directive"; //action Handler
import { findEntities } from "../common/find-entities";
import { handleAction } from "../common/handle-action";
import { hasAction } from "../common/has-action";
import { hasConfigOrEntityChanged } from "../common/has-changed";
import { createEntityNotFoundWarning } from "../components/hui-warning";
import { LovelaceCard, LovelaceCardEditor } from "../types";
import { LightCardConfig } from "./types";
//import { mdiFlashlightOff } from "@mdi/js"; //new icon project

@customElement("hui-light-card")
export class HuiLightCard extends LitElement implements LovelaceCard {
  public static async getConfigElement(): Promise<LovelaceCardEditor> {
    await import("../editor/config-elements/hui-light-card-editor");
    return document.createElement("hui-light-card-editor");
  }

  public static getStubConfig(
    hass: HomeAssistant,
    entities: string[],
    entitiesFallback: string[]
  ): LightCardConfig {
    const includeDomains = ["light"];
    const maxEntities = 1;
    const foundEntities = findEntities(
      hass,
      maxEntities,
      entities,
      entitiesFallback,
      includeDomains
    );

    return { type: "light", entity: foundEntities[0] || "" };
  }

  @property({ attribute: false }) public hass?: HomeAssistant;

  @state() private _config?: LightCardConfig;

  private _brightnessTimout?: number;

  public getCardSize(): number {
    return 5;
  }

  public setConfig(config: LightCardConfig): void {
    if (!config.entity || config.entity.split(".")[0] !== "light") {
      throw new Error("Specify an entity from within the light domain");
    }

    this._config = {
      tap_action: { action: "toggle" },
      old_action: { action: "more-info" },
      ...config,
    };
  }

  protected render(): TemplateResult {
    if (!this.hass || !this._config) {
      return html``;
    }

    const stateObj = this.hass.states[this._config!.entity] as LightEntity;

    if (!stateObj) {
      return html`
        <hui-warning>
          ${createEntityNotFoundWarning(this.hass, this._config.entity)}
        </hui-warning>
      `;
    }

    const brightness =
      Math.round((stateObj.attributes.brightness / 255) * 100) || 0;

    return html`
      <ha-card
      class="hasscard ${classMap({
        "state-on": stateObj.state === "on",
      })}"
      >
        <mwc-icon-button
          class="more-info"
          label="Open more info"
          @click=${this._handleMoreInfo}
          tabindex="0"
        >
          <ha-svg-icon .path=${mdiDotsVertical}></ha-svg-icon>
        </mwc-icon-button>

        <div class="content">
          <div id="controls">
            <div id="slider">
              <round-slider
                min="1"
                max="100"
                .value=${brightness}
                .disabled=${UNAVAILABLE_STATES.includes(stateObj.state)}
                @value-changing=${this._dragEvent}
                @value-changed=${this._setBrightness}
                style=${styleMap({
                  visibility: lightSupportsDimming(stateObj)
                    ? "visible"
                    : "hidden",
                })}
              ></round-slider>
              <ha-icon-button
                class="light-button ${classMap({
                  "slider-center": lightSupportsDimming(stateObj),
                  "state-on": stateObj.state === "on",
                  "state-off": stateObj.state === "off",
                  "state-unavailable": stateObj.state === UNAVAILABLE,
                })}"
                .icon=${this._config.icon || stateIcon(stateObj)}
                .disabled=${UNAVAILABLE_STATES.includes(stateObj.state)}
                style=${styleMap({
                  filter: this._computeBrightness(stateObj),
                  color: this._computeColor(stateObj),
                })}
                @action=${this._handleAction}
                .actionHandler=${actionHandler({
                  hasHold: hasAction(this._config!.hold_action),
                  hasDoubleClick: hasAction(this._config!.double_tap_action),
                })}
                tabindex="0"
              ></ha-icon-button>

            </div>
          </div>

          <div id="info">
            ${UNAVAILABLE_STATES.includes(stateObj.state)
              ? html`
                  <div>
                    ${computeStateDisplay(
                      this.hass.localize,
                      stateObj,
                      this.hass.locale
                    )}
                  </div>
                `
              : html` <div class="brightness">%</div> `}
            ${this._config.name || computeStateName(stateObj)}
          </div>
        </div>
      </ha-card>
    `;
  }

  protected (changedProps: PropertyValues): boolean {
    return hasConfigOrEntityChanged(this, changedProps);
  }

  protected updated(changedProps: PropertyValues): void {
    super.updated(changedProps);
    if (!this._config || !this.hass) {
      return;
    }

    const stateObj = this.hass!.states[this._config!.entity];

    if (!stateObj) {
      return;
    }

    const oldHass = changedProps.get("hass") as HomeAssistant | undefined;
    const oldConfig = changedProps.get("_config") as
      | LightCardConfig
      | undefined;

    if (
      !oldHass ||
      !oldConfig ||
      oldHass.themes !== this.hass.themes ||
      oldConfig.theme !== this._config.theme
    ) {
      applyThemesOnElement(this, this.hass.themes, this._config.theme);
    }
  }

  private _dragEvent(e: any): void {
    this.shadowRoot!.querySelector(
      ".brightness"
    )!.innerHTML = `${e.detail.value} %`;
    this._showBrightness();
    this._hideBrightness();
  }

  private _showBrightness(): void {
    clearTimeout(this._brightnessTimout);
    this.shadowRoot!.querySelector(".brightness")!.classList.add(
      "show_brightness"
    );
  }

  private _hideBrightness(): void {
    this._brightnessTimout = window.setTimeout(() => {
      this.shadowRoot!.querySelector(".brightness")!.classList.remove(
        "show_brightness"
      );
    }, 500);
  }

  private _setBrightness(e: any): void {
    this.hass!.callService("light", "turn_on", {
      entity_id: this._config!.entity,
      brightness_pct: e.detail.value,
    });
  }

  private _computeBrightness(stateObj: LightEntity): string {
    if (stateObj.state === "off" || !stateObj.attributes.brightness) {
      return "";
    }
    const brightness = stateObj.attributes.brightness;
    return `brightness(${(brightness + 245) / 5}%)`;
  }

  private _computeColor(stateObj: LightEntity): string {
    if (stateObj.state === "off") {
      return "";
    }
    return stateObj.attributes.rgb_color
      ? `rgb(${stateObj.attributes.rgb_color.join(",")})`
      : "";
  }

  private _handleAction(ev: ActionHandlerEvent) {
    handleAction(this, this.hass!, this._config!, ev.detail.action!);
  }

  private _handleMoreInfo() {
    fireEvent(this, "hass-more-info", {
      entityId: this._config!.entity,
    });
  }

  static get styles(): CSSResultGroup {
    return css`
      ha-card {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
        text-align: center;
        --name-font-size: 1.2rem;
        --brightness-font-size: 1.2rem;
        background: rgba(120,120,120,0.7);
        color: white;
        border-radius: 25px;
      }

      .more-info {
        position: absolute;
        cursor: pointer;
        top: 0;
        right: 0;
        border-radius: 100%;
        color: var(--secondary-text-color);
        z-index: 1;
      }

      .content {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }

      #controls {
        display: flex;
        justify-content: center;
        padding: 16px;
        position: relative;
      }

      #slider {
        height: 100%;
        width: 100%;
        position: relative;
        max-width: 200px;
        min-width: 100px;
      }

      round-slider {
        --round-slider-path-color: var(--disabled-text-color);
        --round-slider-bar-color: var(--primary-color);
        padding-bottom: 10%;
      }

      .light-button {
        color: var(--paper-item-icon-color, #44739e);
        width: 100%;
        height: auto;
        position: absolute;
        max-width: calc(60% - 40px);
        box-sizing: border-box;
        border-radius: 100%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        --mdc-icon-button-size: 100%;
        --mdc-icon-size: 100%;


      }

      .light-button.state-on {
        color: var(--paper-item-icon-active-color, #fdd835);
        animation: shake 0.9s;
        animation-iteration-count: 1;
      }

      .light-button.state-off {


      }
      @keyframes shake {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        10% { transform: translate(-50%, -50%) rotate(25deg); }
        20% { transform: translate(-50%, -50%) rotate(0deg); }
        30% { transform: translate(-50%, -50%) rotate(-25deg); }
        40% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-50%, -50%) rotate(25deg); }
        60% { transform: translate(-50%, -50%) rotate(0deg); }
        70% { transform: translate(-50%, -50%) rotate(-25deg); }
        80% { transform: translate(-50%, -50%) rotate(0deg); }
        90% { transform: translate(-50%, -50%) rotate(25deg); }
        100% { transform: translate(-50%, -50%) rotate(0deg); }
      }

      .hasscard.state-on {
        background: rgba(255,255,255,0.7);
        color: black;
      }

      .light-button.state-unavailable {
        color: var(--state-icon-unavailable-color);
      }

      #info {
        text-align: center;
        margin-top: -56px;
        padding: 16px;
        font-size: var(--name-font-size);
      }

      .brightness {
        font-size: var(--brightness-font-size);
        opacity: 0;
        transition: opacity 0.5s ease-in-out;
        -moz-transition: opacity 0.5s ease-in-out;
        -webkit-transition: opacity 0.5s ease-in-out;
      }

      .show_brightness {
        opacity: 1;
      }
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "hui-light-card": HuiLightCard;
  }
}
